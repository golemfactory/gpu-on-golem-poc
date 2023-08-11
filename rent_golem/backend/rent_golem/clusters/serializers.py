from rest_framework import serializers
from .models import Clusters


class ClustersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clusters
        fields = ['uuid', 'package_type', 'status', 'additional_params', 'size', 'created_at', 'last_update']
