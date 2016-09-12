from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponseServerError
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST, require_GET

from events.models import Event, Team


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


def create_team(request, event_id: int):
    raise HttpResponseServerError('501: Not yet implemented!')


def teams(request, event_id: int):
    raise HttpResponseServerError('501: Not yet implemented!')

