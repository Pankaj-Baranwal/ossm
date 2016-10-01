from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import TemplateView
from django.views.defaults import (page_not_found, server_error,
        bad_request, permission_denied)

from . import views, admin


urlpatterns = [
    url(r'^admin/', admin.urls),
    url(r'^', include('landing.urls')),
    url(r'^api/v1/', include('ossm.api', namespace='api')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/', include('people.urls')),
    url(r'^events/', include('events.urls')),

    # Static routes:
    url(r'^privacy-policy/$',
        TemplateView.as_view(template_name='privacy_policy.html'),
        name='privacy_policy'),

    # Support old routes.
    url(r'^email_read/$', views.email_read, name='email_track')
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^playground/$',
            TemplateView.as_view(template_name='playground.html'),
            name='playground'),
        url(r'^400/$', bad_request, kwargs=dict(exception={})),
        url(r'^403/$', permission_denied, kwargs=dict(exception={})),
        url(r'^404/$', page_not_found, kwargs=dict(exception={})),
        url(r'^500/$', server_error),
    ]

