from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework import viewsets, mixins


# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.forms import TeamForm
from events.models import Event, Team
from events.permissions import IsTeamMember
from events.serializers import TeamSerializer
from people.models import User
from people.permissions import IsOwnerOrReadOnly


@require_GET
def get_event(request, event_id: int):
    response = {
        'user': request.user,
        'event': Event.objects.filter(id=event_id).first()
    }
    if request.user.is_authenticated():
        if request.user.teams.filter(event=event_id).exists():
            response.registered = True
            response.team = request.user.teams.all().filter(event=event_id).first()
    return render(request, 'event.html', response)


@login_required
@require_POST
def register(request, event_id: int):
    response = {}
    if not Event.objects.filter(id=event_id).exists():
        raise Http404("Event doesn't exists.")
    response['event'] = Event.objects.filter(id=event_id).first()
    team = Team()
    team.event = event_id
    team.save()
    request.user.teams.add(team)
    request.user.save()
    response['user'] = request.user
    return JsonResponse(response)


@login_required
@csrf_exempt
def register_api(request, event_id: int):
    if not Event.objects.filter(id=event_id).exists():
        raise Http404("Event doesn't exists.")
    if request.user.teams.filter(event=event_id).exists():
        raise Exception('Already registered.')
    team = Team()
    team.event = event_id
    team.members.add(User.objects.filter(username=request.user.username).first())
    team.save()
    return JsonResponse(object(), status=201)


class TeamApiViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = 'nickname'
    permission_classes = (IsAuthenticated, IsTeamMember, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(Q(first_member=request.user.username) | Q(second_member=request.user.username)).all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Team.objects.filter(Q(event__code=request.POST.get('event')) &
                               (Q(first_member__username=request.user.username) |
                                Q(second_member__username=request.user.username))):
            return HttpResponseBadRequest('Already registered!')

        serializer.save(owner=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TeamView(TemplateView):
    template_name = 'team.html'
    permission_classes = (IsAuthenticated, )

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'title': self.title
        }

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.form = TeamForm()
        self.title = 'Create a team'
        if 'team' in request.GET:
            self.title = 'Edit team'
            team = Team.objects.get(nickname=request.GET['team'])
            if team and self.user in [team.first_member, team.second_member]:
                self.form = TeamForm(instance=team)
            else:
                raise Http404('Team not found!')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        if 'team' in request.GET:
            team = Team.objects.get(nickname=request.GET['team'])
            if team and self.user in [team.first_member, team.second_member]:
                self.team = team
                self.form = TeamForm(request.POST, instance=self.team)
        else:
            self.form = TeamForm(request.POST)
        if self.form.is_valid():
            self.form.save()
        else:
            return self.render_to_response(self.form.errors)
        self.title = '%s // Team' % self.form.instance.nickname
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
