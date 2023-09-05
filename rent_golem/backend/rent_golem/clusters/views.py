from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Cluster
from .serializers import ClusterSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    def destroy(self, request, *args, **kwargs):
        cluster = Cluster.objects.filter(uuid=kwargs["pk"]).first()
        if request.user.is_authenticated:
            if cluster.owner == request.user:
                cluster.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        cluster = Cluster.objects.filter(uuid=kwargs["pk"]).first()

        if request.user.is_authenticated:
            if cluster.owner == request.user:
                if set(request.data.keys()) != {'size'}:
                    return Response(
                        status=status.HTTP_403_FORBIDDEN,
                        data={"message": "You can only change 'size' parameter."}
                    )
                cluster.size = request.data['size']
                cluster.save()
                return Response(status=status.HTTP_202_ACCEPTED, data=request.data)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
