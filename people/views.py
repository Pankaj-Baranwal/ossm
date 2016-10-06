from django.views.generic import TemplateView
from rest_framework import viewsets, mixins
from django.db.models import Q

from events.models import Team, Event
from people.forms import ProfileForm, HackerrankForm, DataWeaveForm
from people.permissions import IsOwnerOrReadOnly
from .models import User, Subscription, Contestant
from .serializers import UserSerializer, SubscriptionSerializer


class Dashboard(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        return {
            'events': self.events,
            'teams': self.teams
        }

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.teams = Team.objects.filter(Q(first_member=self.user.username) | Q(second_member=self.user.username)).all()
        self.events = Event.objects.all()
        for event in self.events:
            event.set_registered(self.user)
            event.set_team(self.user)
        return super().get(request, *args, **kwargs)


class Profile(TemplateView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form
        }

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.form = ProfileForm(request.POST, instance=self.user)
        if self.form.is_valid():
            self.form.save()
        self.form = ProfileForm(instance=self.user)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.form = ProfileForm(instance=self.user)
        return super().get(request, *args, **kwargs)


class SubscriptionApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API end-points that allows subscriptions to be viewed or edited.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = ()


class SelfApiView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API end-points that allows user to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsOwnerOrReadOnly, )


class HackerRankView(TemplateView):
    template_name = 'hackerrank.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form
        }

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.contestant = Contestant.objects.get(user=self.user)
        self.form = HackerrankForm(instance=self.contestant)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.contestant = Contestant.objects.get(user=self.user)
        self.hackerrank = "" + self.contestant.hackerrank
        self.form = HackerrankForm(request.POST, instance=self.contestant)
        if self.form.is_valid(hackerrank=self.hackerrank):
            self.form.save()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DataWeaveView(TemplateView):
    template_name = 'data_weave.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form
        }

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.data_weave = Contestant.objects.get(user=self.user)
        self.form = DataWeaveForm(instance=self.data_weave)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.contestant = Contestant.objects.get(user=self.user)
        self.data_weave = "" + str(self.contestant.data_weave)
        self.form = DataWeaveForm(request.POST, instance=self.contestant)

        """
        Check if it is a valid gist, run and calculate accuracy.
        """
        if self.form.is_valid(data_weave=self.data_weave):
            self.form.save()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
