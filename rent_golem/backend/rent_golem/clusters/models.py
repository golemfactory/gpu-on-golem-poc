from urllib.parse import urljoin
import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import User
from clusters.managers import ExistingClusterManager

class Cluster(models.Model):
    class Package(models.TextChoices):
        AUTOMATIC = 'automatic'

    class Status(models.TextChoices):
        PENDING = 'pending'  # When machine has no active workers
        RUNNING = 'running'  # When at least one worker is running
        SHUTTING_DOWN = 'shutting-down'  # When user issued to terminate cluster
        TERMINATED = 'terminated'  # When cluster runner finished

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    package = models.CharField(max_length=255, choices=Package.choices)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING)
    additional_params = models.JSONField(blank=True, default=dict)
    size = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(settings.MAX_CLUSTER_SIZE)],
        help_text="Number of desired workers.",
    )
    address = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    existing_objects = ExistingClusterManager()

    def __str__(self):
        return f'ID: {self.pk}, {self.size} x {self.package} [{self.status}]'

    @property
    def short_id(self):
        return str(self.id).split('-')[-1]


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
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.STARTING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint("provider", "service_id", name="unique_provider_service_id"),
        ]

    @property
    def healthcheck_url(self):
        package_to_healthcheck_path = {
            Cluster.Package.AUTOMATIC: "/sdapi/v1/sd-models",
        }
        return urljoin(f'https://{self.address}', package_to_healthcheck_path[self.cluster.package])

    def __str__(self):
        return f'ID: {self.id} Cluster_id: {self.cluster_id} [{self.provider}] -> {self.address}'
