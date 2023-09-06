from django.db import models


class ExistingClusterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_deleted=True)
