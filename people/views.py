import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.shortcuts import render

# Create your views here.
from events.models import Team, Event
from ossm.exceptions import Http409
from people.models import User


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user
    })


@login_required
def create_team(request, event_id: int):
    try:
        body = json.loads(request.body.decode('utf-8'))
    except:
        raise HttpResponseBadRequest('Invalid JSON body')
    if Team.objects.filter(nickname=body['handle']).exists():
        raise Http409('Team handle already exists!')
    team = Team()
    team.event = Event.objects.filter(id=event_id).first()
    team.name = body['name']
    team.nickname = body['handle']
    team.members.add(User.objects.filter(email=request.user.email))
    for team_member in team['members']:
        # if not User.objects.filter(email=team_member).exists():
        pass
    raise HttpResponseServerError('501: Not yet implemented!')


def teams(request, event_id: int):
    response = {}
    response['teams'] = Team.objects.filter(event=event_id).all()
    return render(request, 'teams.html', response)
