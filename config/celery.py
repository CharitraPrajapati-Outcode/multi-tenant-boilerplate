import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("django_celery")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.timezone = 'America/New_York'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')