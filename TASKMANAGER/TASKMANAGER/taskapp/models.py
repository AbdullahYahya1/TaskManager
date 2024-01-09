from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
class DayTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_tasks')
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    estimated_time = models.CharField(max_length=5, blank=True, null=True)  # New field for estimated time
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class WeeklyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_tasks')
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    estimated_time = models.CharField(max_length=5, blank=True, null=True)  # New field for estimated time

    def __str__(self):
        return self.title

class MonthlyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_tasks')
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    estimated_time = models.CharField(max_length=5, blank=True, null=True)  # New field for estimated time

    def __str__(self):
        return self.title

class SharedUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_sharer')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_shared_with')

    def __str__(self):
        return f"{self.owner.username} shares with {self.shared_with.username}"
