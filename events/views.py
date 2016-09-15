from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json


# Create your views here.

from events.models import Event, Team
from ossm.exceptions import Http409
from people.models import User


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
