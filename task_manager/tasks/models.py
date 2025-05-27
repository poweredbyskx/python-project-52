from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks_created'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_executed'
    )
    labels = models.ManyToManyField(Label, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __str__(self):
        full_name = self.get_full_name()  # first_name + last_name
        return full_name if full_name else self.username

