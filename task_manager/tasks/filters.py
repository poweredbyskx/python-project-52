import django_filters
from django_filters import FilterSet, BooleanFilter
from django.forms import CheckboxInput
from django.utils.translation import gettext

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskFilter(FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=gettext('status')
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=gettext('executor')
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label=gettext('labels')
    )
    only_own_tasks = BooleanFilter(
        method='filter_only_own',
        label=gettext('only_my_tasks'),
        widget=CheckboxInput()
    )

    def __init__(self, data=None, *args, **kwargs):
        if data is not None and isinstance(data, QueryDict):
            mutable_data = data.copy()
            if 'labels' in mutable_data and not isinstance(mutable_data.getlist('labels'), list):
                # Не обязательно, но безопасно
                mutable_data.setlist('labels', mutable_data.getlist('labels'))
            data = mutable_data
        super().__init__(data, *args, **kwargs)

    def filter_only_own(self, queryset, name, value):
        request = self.request
        if value and request and request.user.is_authenticated:
            return queryset.filter(author=request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'only_own_tasks']
