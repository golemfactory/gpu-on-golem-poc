from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from clusters.models import Cluster
from clusters.serializers import ClusterSerializer, ClusterUpdateSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthenticated]
    queryset = Cluster.existing_objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ClusterUpdateSerializer
        else:
            return ClusterSerializer

    def destroy(self, request, *args, **kwargs):
        cluster = self.get_object()
        if cluster.owner == request.user:
            cluster.is_deleted = True
            cluster.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        cluster = self.get_object()
        if cluster.owner == request.user:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(cluster, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(cluster, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                cluster._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
