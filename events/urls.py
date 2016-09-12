from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^(?P<event_id>[0-9])$', views.get_event),
    url(r'^(?P<event_id>[0-9])/register/$', views.register),
    url(r'^(?P<event_id>[0-9])/teams/$', views.teams),
    url(r'^(?P<event_id>[0-9])/teams/new$', views.teams),
]
