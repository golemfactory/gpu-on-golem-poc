from rest_framework import serializers
from . models import Clusters

class ClustersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clusters
        fields = '__all__'  # TODO Explicit all params