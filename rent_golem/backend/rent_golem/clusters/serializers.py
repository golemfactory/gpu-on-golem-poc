from rest_framework import serializers

from clusters.models import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['uuid', 'owner', 'package', 'status', 'additional_params', 'size', 'created_at', 'last_update']


class ClusterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['size']
