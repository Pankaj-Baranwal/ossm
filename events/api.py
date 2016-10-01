from rest_framework.routers import SimpleRouter

from events.views import TeamApiViewSet
from ossm.api import api_root


router = SimpleRouter()
router.register(r'^teams', TeamApiViewSet)

api_root.register(router)
