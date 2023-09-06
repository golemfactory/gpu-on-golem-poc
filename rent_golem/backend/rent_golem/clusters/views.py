from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Cluster
from .serializers import ClusterSerializer, ClusterUpdateSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    queryset = Cluster.existing_objects.all()

    serializer_class = ClusterSerializer

    def list(self, request, *args, **kwargs):
        print("DUDUDUDUUUUUUPA")
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            print("DUUPA")
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ClusterSerializer(self.queryset, many=True)
        return Response(serializer.data)

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
            serializer = ClusterUpdateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            cluster.size = request.data['size']
            cluster.save()
            return Response(status=status.HTTP_202_ACCEPTED, data=request.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
