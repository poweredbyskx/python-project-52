from django import forms
from django.forms import ModelForm
from .models import Task
from django.utils.translation import gettext
import django_filters
from django_filters import FilterSet, BooleanFilter
from django.forms import CheckboxInput

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


class TaskFilter(FilterSet):
    only_own_tasks = BooleanFilter(
        method='filter_only_own',
        label='only_my_tasks',
        widget=CheckboxInput(),
    )

    def filter_only_own(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
