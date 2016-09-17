from django.conf.urls import url, include

from ossm import views
from ossm.social_rest_auth import FacebookLogin, GoogleLogin
from ossm import admin

urlpatterns = [
    url(r'^admin/', admin.urls),
    url(r'^', include('landing.urls')),
    url(r'events/', include('events.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/', include('people.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='g_login'),
    url(r'^rest-auth/github/$', GoogleLogin.as_view(), name='gh_login'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^email_read/$', views.email_read, name='email_track')
]
