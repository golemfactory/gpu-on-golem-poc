from rest_framework import viewsets

from .models import Cluster
from .serializers import ClusterSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
