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
    user_profile = User.objects.filter(email=request.user.email).first()
    if request.method == 'POST':
        u = request.POST
        if request.user.username != u['username'] and User.objects.filter(username=u['username']).exists():
            raise Exception("Username already exists.")
        if request.user.email != u['email'] and User.objects.filter(email=u['email']).exists():
            raise Exception("Email already registered.")
        user_profile.username = u['username']
        user_profile.email = u['email']
        user_profile.first_name = u['first_name']
        user_profile.last_name = u['last_name']
        user_profile.contact = int(u['contact']) if u['contact'] != '' else 0
        user_profile.city = u['city']
        user_profile.state = u['state']
        user_profile.institute = u['institute']
        user_profile.save()
        user_profile = User.objects.filter(email=u['email']).first()
    return render(request, 'profile.html', {
        'user': user_profile
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
