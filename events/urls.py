from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^(?P<event_id>[0-9])$', views.get_event),
    url(r'^(?P<event_id>[0-9])/register/$', views.register_api),
    url(r'^team/new$', views.TeamView.as_view(), name='new_team'),
    url(r'^team/edit$', views.TeamView.as_view(), name='edit_team'),
]
