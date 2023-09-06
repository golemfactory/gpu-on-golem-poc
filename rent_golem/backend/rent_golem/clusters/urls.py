from rest_framework import routers

from clusters.views import ClusterViewSet


router = routers.SimpleRouter()
router.register(r'', ClusterViewSet)

urlpatterns = router.urls
