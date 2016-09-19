import importlib

from django.conf import settings
from django.conf.urls import include, url
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from .social_rest_auth import FacebookLogin, GoogleLogin


class APIRoot(object):
    routes = []
    def register(self, router):
        self.routes.append(router)

    def get_urls(self):
        urls = []
        for router in self.routes:
            for url in router.urls:
                urls.append(url)
        return urls

api_root = APIRoot()

for app in settings.INSTALLED_APPS:
    try:
        importlib.import_module('%s.api' % app)
    except ImportError:
        pass

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator()
    return response.Response(generator.get_schema(request=request))


urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/account/', include('rest_auth.registration.urls')),
    url(r'^auth/social/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^auth/social/google/$', GoogleLogin.as_view(), name='g_login'),
    url(r'^auth/social/github/$', GoogleLogin.as_view(), name='gh_login'),
    url(r'^', include(api_root.get_urls())),
    url(r'^', schema_view),
]
