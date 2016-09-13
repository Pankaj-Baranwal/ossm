from django.conf.urls import url
from people import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/api$', views.profile_api, name='profile_api')
]
