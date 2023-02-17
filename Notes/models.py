import json
from datetime import datetime, timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from user_auth.models import CustomUser


# Create your models here.
class Labels(models.Model):
    """
     Labels Model : name, user_id, created_at, modified_at
    """
    name = models.CharField(max_length=150, unique=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Notes(models.Model):
    """
            Notes Model : title, description, user_id, created_at, modified_at, collaborator, label...
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(CustomUser, related_name='collaborator')
    label = models.ManyToManyField(Labels)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    color = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='notes_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Note"


@receiver(post_save, sender=Notes)
def reminder_handler(sender, instance, **kwargs):
    if instance.reminder:
        current_date = datetime.now()
        reminder_date = instance.reminder.date()
        no_of_days = (reminder_date - current_date.date()).days
        reminder_time = datetime.now() + timedelta(days=no_of_days)
        # Schedule the reminder task using Celery
        schedule_task(instance, reminder_time)


def schedule_task(instance, reminder_time):
    schedule, created = CrontabSchedule.objects.get_or_create(
        hour=instance.reminder.hour,
        minute=instance.reminder.minute,
        day_of_month=reminder_time.day,  # 1-31 and we will not able to give no of days
        month_of_year=instance.reminder.month
    )

    existing_task = PeriodicTask.objects.filter(name=f"Task for note {instance.id}").first()
    if existing_task is not None:
        existing_task.crontab = schedule
        existing_task.save()

    else:
        new_task = PeriodicTask.objects.create(
            crontab=schedule,
            name=f"Task for note {instance.id}",
            task='Notes.tasks.send_mail_func',
            args=json.dumps([
                instance.title,
                instance.description,
                [instance.user.email]
            ])),
