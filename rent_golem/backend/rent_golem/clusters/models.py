from django.db import models


class Cluster(models.Model):
    class Package(models.TextChoices):
        AUTOMATIC = 'automatic'
        CUSTOM_AUTOMATIC = 'automatic-custom'
        TEXT_GEN_WEBUI = 'text-gen-webui'
        JUPYTER = 'jupyter'
        PYTORCH = 'pytorch'

    class Status(models.TextChoices):
        STARTING = 'Starting'
        STOPPING = 'Stopping'
        STOPPED = 'Stopped'
        CONTINUING = 'Continuing'
        TERMINATING = 'Terminating'
        TERMINATED = 'Terminated'

    uuid = models.UUIDField(primary_key=True)
    package_type = models.CharField(max_length=255, choices=Package.choices, default=Package.JUPYTER)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.STARTING)
    # https://stackoverflow.com/questions/67469569/using-django-jsonfield-in-model -> possible JSON Schema
    additional_params = models.JSONField()
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
