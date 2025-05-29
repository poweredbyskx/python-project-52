import django_filters
from django_filters import FilterSet, BooleanFilter
from django.forms import CheckboxInput
from django.http import QueryDict
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class TaskFilter(FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label=_("Статус")
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label=_("Исполнитель"), empty_label=_("----------")
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(), label=_("Метка")
    )
    only_own_tasks = BooleanFilter(
        method="filter_only_own", label=_("Только свои задачи"), widget=CheckboxInput()
    )

    def __init__(self, data=None, *args, **kwargs):
        if data is not None and isinstance(data, QueryDict):
            mutable_data = data.copy()
            if "labels" in mutable_data and not isinstance(
                mutable_data.getlist("labels"), list
            ):
                # Не обязательно, но безопасно
                mutable_data.setlist("labels", mutable_data.getlist("labels"))
            data = mutable_data
        super().__init__(data, *args, **kwargs)

    def filter_only_own(self, queryset, name, value):
        request = self.request
        if value and request and request.user.is_authenticated:
            return queryset.filter(author=request.user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]
