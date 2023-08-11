from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Clusters
from .serializers import ClustersSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def manage_cluster(request):
    person = {'name': 'Jakub', 'age': 24}
    return Response(person)

@api_view(['GET'])
def get_clusters_data(request):
    clusters = Clusters.objects.all()
    serializer = ClustersSerializer(clusters, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_clusters_object(request):
    serializer = ClustersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
