from django.contrib.auth.models import User
from django.core.mail import send_mail

from application.celery import app

from .utils import send


# celery -A application worker -l info
@app.task
def send_spam_email(user_email):
    send(user_email)


# celery -A application beat -l info
@app.task
def send_beat_email():
    for user in User.objects.filter(is_staff=False):
        send_mail(
            'You are subscribed to the newsletter',
            'we will send you emails every few minutes for a test',
            'vp3231963@gmail.com',
            [user.email],
            fail_silently=False,
        )
