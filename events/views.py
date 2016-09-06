from django.shortcuts import render

# Create your views here.
from events.models import Event


def get_event(request, event_id):
    response = {
        'user': request.user,
        'event': Event.objects.filter(id=event_id).first()
    }
    if request.user.is_authenticated():
        if request.user.teams.filter(event=event_id).exists():
            response.registered = True
            response.team = request.user.teams.all().filter(event=event_id).first()
    return render(request, 'event.html', response)
