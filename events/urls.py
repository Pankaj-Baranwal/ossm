from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from events import views

urlpatterns = [
    url(r'^(?P<event_id>[0-9])$', views.get_event),
    url(r'^(?P<event_id>[0-9])/register/$', views.register_api),
    url(r'^$', views.events),
    url(r'^team/$', views.TeamView.as_view(), name='team'),
    url(r'^register/$', views.Register.as_view(), name='register_individual')
]
