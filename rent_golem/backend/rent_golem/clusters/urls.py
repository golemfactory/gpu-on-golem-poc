from rest_framework import routers

from clusters.views import ClustersViewSet


router = routers.SimpleRouter()
router.register(r'', ClustersViewSet)

urlpatterns = router.urls
