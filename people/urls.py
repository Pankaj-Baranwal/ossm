from django.conf.urls import url, include

from people import views


urlpatterns = [
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^$', views.dashboard, name='dashboard'),
]
