from django.conf.urls import url, include
from rest_framework import routers

from people import views

router = routers.DefaultRouter()
# router.register(r'^subscriptions', views.SubscriptionViewSet)
router.register(r'user', views.UserApiView)

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/api$', views.profile_api, name='profile_api'),
    url(r'^api/me', views.UserApiView.as_view())
]
