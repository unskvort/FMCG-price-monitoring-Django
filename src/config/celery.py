import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


app = Celery("config")  # type: ignore

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
# RUN command: celery -A config worker --beat -l info
app.conf.beat_schedule = {
    "update-store-everyday": {
        "task": "store.tasks.update_store",
        "schedule": settings.TASK_RECURRENCE_PERIOD,
        "args": (),
    },
}

app.conf.timezone = settings.TIME_ZONE
