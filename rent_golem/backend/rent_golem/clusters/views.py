from rest_framework import viewsets

from .models import Clusters
from .serializers import ClustersSerializer


class ClustersViewSet(viewsets.ModelViewSet):
    queryset = Clusters.objects.all()
    serializer_class = ClustersSerializer
