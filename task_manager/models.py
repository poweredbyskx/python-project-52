from django.db import models
from django.contrib.auth.models import User

# Модель Label
class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Модель Status
class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Модель Task
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    labels = models.ManyToManyField(Label, through='Task_labels', blank=True)  # Используем промежуточную модель
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

# Промежуточная модель Task_labels для связи Task и Label
class Task_labels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # внешний ключ на модель Task
    label = models.ForeignKey(Label, on_delete=models.CASCADE)  # внешний ключ на модель Label

    class Meta:
        # Устанавливаем имя таблицы, чтобы избежать конфликта с таблицей ManyToMany
        db_table = 'task_manager_task_labels'
