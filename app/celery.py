import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cereal_assignment.settings")

app = Celery("cereal_assignment")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()