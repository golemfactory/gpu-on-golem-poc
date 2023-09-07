from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from clusters.filters import IsOwnerFilterBackend
from clusters.models import Cluster
from clusters.serializers import ClusterSerializer, ClusterUpdateSerializer
from clusters.tasks import run_cluster


class ClusterViewSet(viewsets.ModelViewSet):
    filter_backends = [IsOwnerFilterBackend]
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]
    queryset = Cluster.existing_objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ClusterUpdateSerializer
        else:
            return ClusterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        run_cluster.delay(str(instance.pk))

    def perform_destroy(self, cluster):
        cluster.is_deleted = True
        cluster.save()
