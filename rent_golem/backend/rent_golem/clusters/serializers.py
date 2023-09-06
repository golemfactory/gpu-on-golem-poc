from rest_framework import serializers

from clusters.models import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cluster
        fields = ('id', 'owner', 'package', 'status', 'additional_params', 'size', 'created_at', 'last_update')
        read_only_fields = ('id', 'status', 'created_at', 'last_update')


class ClusterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('size', )
