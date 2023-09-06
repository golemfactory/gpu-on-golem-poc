from rest_framework import viewsets

from clusters.models import Cluster
from clusters.serializers import ClusterSerializer
from clusters.tasks import run_cluster


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        run_cluster.delay(str(instance.pk))
