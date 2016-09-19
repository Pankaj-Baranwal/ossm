from rest_framework.routers import SimpleRouter

from ossm.api import api_root
from .views import SubscriptionApiView, SelfApiView


router = SimpleRouter()
router.register(r'people/subscription', SubscriptionApiView)
router.register(r'people', SelfApiView)

api_root.register(router)
