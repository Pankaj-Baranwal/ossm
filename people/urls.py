from django.conf.urls import url, include

from people import views


urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/api$', views.profile_api, name='profile_api'),
    url(r'^api/me', views.SelfApiView.as_view())
]
