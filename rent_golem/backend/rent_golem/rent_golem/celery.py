import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_golem.settings')
app = Celery('rent_golem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
