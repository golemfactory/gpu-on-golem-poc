from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models



class Cluster(models.Model):
    class Package(models.TextChoices):
        AUTOMATIC = 'automatic'
        CUSTOM_AUTOMATIC = 'automatic-custom'
        TEXT_GEN_WEBUI = 'text-gen-webui'
        JUPYTER = 'jupyter'
        PYTORCH = 'pytorch'

    class Status(models.TextChoices):
        PENDING = 'pending'  # When machine has no active workers
        RUNNING = 'running'  # When at least one worker is running
        SHUTTING_DOWN = 'shutting-down'  # When user issued to terminate cluster
        TERMINATED = 'terminated'  # When cluster runner finished

    uuid = models.UUIDField(primary_key=True)
    package_type = models.CharField(max_length=255, choices=Package.choices)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING)
    additional_params = models.JSONField()
    size = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(settings.MAX_CLUSTER_SIZE)],
        help_text="Number of desired workers.",
    )
    address = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


class Provider(models.TextChoices):
    RUNPOD = 'runpod'


class Worker(models.Model):
    class Status(models.TextChoices):
        STARTING = 'starting'
        OK = 'ok'
        BAD = 'bad'

    cluster = models.ForeignKey(Cluster, null=True, on_delete=models.SET_NULL, related_name='workers')
    provider = models.CharField(max_length=255, choices=Provider.choices)
    address = models.CharField(max_length=1000, null=True)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.STARTING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
