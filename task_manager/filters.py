import django_filters
from .models import Task, Label
from django.contrib.auth.models import User

class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains', label='Статус')
    assignee = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
    labels = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(), label='Метки')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Автор задачи')

    class Meta:
        model = Task
        fields = ['status', 'assignee', 'labels', 'author']
