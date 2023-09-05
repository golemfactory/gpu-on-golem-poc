from rest_framework import serializers
from .models import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['uuid', 'owner', 'package_type', 'status', 'additional_params', 'size']
