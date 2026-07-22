import os
from celery import Celery

# Point Celery to your Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Create the Celery app
app = Celery("config")

# Tell Celery to read configurations from your settings.py (looking for variables starting with 'CELERY_')
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically find background tasks in your apps
app.autodiscover_tasks()
