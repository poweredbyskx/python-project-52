from .filters import TaskFilter
from django import forms
from django.forms import ModelForm
from .models import Task
from django.utils.translation import gettext

class TaskCreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            "name": gettext("status_name"),
            "description": gettext("task_description"),
            "status": gettext("status"),
            "executor": gettext("executor"),
            "labels": gettext("labels"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
