from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FundooNotes.settings')

app = Celery('FundooNotes')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    # 'send-mail-every-day-at-8':{
    #     'action':'email_app.tasks.send_mail_func',
    #     'schedule':crontab(hour=1, minute=40),
    #      # 'args':(2,)
    }

app.autodiscover_tasks()


@app.task(bind=True)

def debug_task(self):
    print(f'Request: {self.request!r}')
