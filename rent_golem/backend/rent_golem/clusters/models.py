from urllib.parse import urljoin

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
        STOPPED = 'stopped'

    cluster = models.ForeignKey(Cluster, null=True, on_delete=models.SET_NULL, related_name='workers')
    provider = models.CharField(max_length=255, choices=Provider.choices)
    service_id = models.CharField(max_length=255, null=True, help_text="ID of worker in provider space.")
    address = models.CharField(max_length=1000, null=True)
    healthcheck_path = models.CharField(
        max_length=1000,
        null=True,
        help_text="Path relative to address used as healthcheck."
    )
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.STARTING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def healthcheck_url(self):
        return urljoin(self.address, self.healthcheck_path)

    def __str__(self):
        return f'ID: {self.id} Cluster_id: {self.cluster_id} [{self.provider}] -> {self.address}'
