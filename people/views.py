import json

from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import views
from rest_framework.response import Response

from events.models import Team, Event
from ossm.exceptions import Http409
from ossm.views import JSONResponse
from people.models import User, Subscription
from people.serializers import UserSerializer, SubscriptionSerializer


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })


@login_required
def profile(request):
    user_profile = User.objects.filter(username=request.user.username).first()
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
        user_profile = User.objects.filter(username=u['username']).first()
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


@login_required
@csrf_exempt
def profile_api(request):
    if request.method == 'GET':
        user_profile = User.objects.filter(username=request.user.username).first()
        serializer = UserSerializer(user_profile)
        return JSONResponse(serializer.data)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        user_profile = User.objects.filter(username=request.user.username).first()
        if request.user.username != data['username'] and User.objects.filter(username=data['username']).exists():
            raise Exception("Username already exists.")
        if request.user.email != data['email'] and User.objects.filter(email=data['email']).exists():
            raise Exception("Email already registered.")
        user_profile.username = data['username']
        user_profile.email = data['email']
        user_profile.first_name = data['first_name']
        user_profile.last_name = data['last_name']
        user_profile.contact = int(data['contact']) if data['contact'] != '' else 0
        user_profile.city = data['city']
        user_profile.state = data['state']
        user_profile.institute = data['institute']
        user_profile.save()
        user_profile = User.objects.filter(email=data['email']).first()
        serializer = UserSerializer(user_profile)
        return JSONResponse(serializer.data)


class SubscriptionApiView(views.APIView):
    """
    API end-points that allows subscriptions to be viewed or edited.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request):
        email = request.POST['email']
        if email:
            validate_email(email)
            return Response(status=201)
        else:
            return HttpResponseBadRequest('No E-Mail address provided')


class UserApiView(views.APIView):
    """
    API end-points that allows user to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.filter(email=request.user.email).first()
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)
