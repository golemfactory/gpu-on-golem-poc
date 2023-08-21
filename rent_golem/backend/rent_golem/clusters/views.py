from rest_framework import viewsets

from clusters.models import Clusters
from clusters.serializers import ClustersSerializer
from clusters.tasks import run_cluster


class ClustersViewSet(viewsets.ModelViewSet):
    queryset = Clusters.objects.all()
    serializer_class = ClustersSerializer

    def perform_create(self, serializer):
        instance = super().perform_create(serializer)
        run_cluster.apply_async(instance.id)
