import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_schedule = {
    'send_every_2_minute': {
        'task': 'news.tasks.send_beat_email',
        'schedule': crontab(minute='*/2')
    }
}
