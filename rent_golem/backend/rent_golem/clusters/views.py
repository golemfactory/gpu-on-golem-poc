from rest_framework import viewsets

from clusters.models import Clusters
from clusters.serializers import ClustersSerializer


class ClustersViewSet(viewsets.ModelViewSet):
    queryset = Clusters.objects.all()
    serializer_class = ClustersSerializer
