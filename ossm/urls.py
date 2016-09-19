from django.conf.urls import url, include
from django.views.generic import TemplateView

from . import views, admin


urlpatterns = [
    url(r'^admin/', admin.urls),
    url(r'^', include('landing.urls')),
    url(r'^api/v1/', include('ossm.api')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/', include('people.urls')),
    url(r'^events/', include('events.urls')),

    # Static routes:
    url(r'^privacy-policy/$', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),

    # Support old routes.
    url(r'^email_read/$', views.email_read, name='email_track')
]
