from decouple import config
from celery.schedules import crontab


CELERY_BROKER_URL = config('CELERY_BROKER_URL', default="redis://localhost:6379")
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default="redis://localhost:6379")


CELERY_BEAT_SCHEDULE = {
    # 'send-clean-flask-notification-every-day-9am': {
    #     'task': 'apps.user_device.tasks.send_clean_flask_notification',
    #     'schedule': crontab(hour=9, minute=0),
    # },
}