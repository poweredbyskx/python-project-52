from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from task_manager.mixins import EditView
from .models import Task

from .forms import TaskCreationForm
from .filters import TaskFilter


class TasksView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/task_filter.html"
    context_object_name = "object_list"
    filterset_class = TaskFilter

    def get_queryset(self):
        qs = super().get_queryset().order_by("created_at")
        only_own = self.request.GET.get("only_own_tasks")
        if only_own == "1":
            qs = qs.filter(author=self.request.user)
        return qs

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["request"] = self.request  # ← это ключ!
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        only_own = self.request.GET.get("only_own_tasks")
        context["only_own_tasks_selected"] = only_own == "1"
        context["status_id"] = self.request.GET.get("status", "")
        context["executor"] = self.request.GET.get("executor", "")
        context["labels"] = self.request.GET.getlist("labels")
        return context


class TaskFormCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {"form": TaskCreationForm()}
        return render(request, "tasks/new.html", context)

    def post(self, request):
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            task.labels.set(form.cleaned_data["labels"])
            messages.success(request, _("task_created"))  # заменено здесь
            return redirect(reverse_lazy("tasks:list"))
        return render(request, "tasks/new.html", {"form": form})


class TaskForm:
    value = Task
    template = "tasks/edit.html"
    form = TaskCreationForm
    text = "task_edit"
    path = "tasks"


class TaskFormEditView(LoginRequiredMixin, View, TaskForm, EditView):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        labels = task.labels.all()
        form = TaskCreationForm(instance=task)
        return render(
            request,
            "tasks/edit.html",
            {"form": form, "task_id": task_id, "task": task, "labels": labels},
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        form = TaskCreationForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            task.labels.set(form.cleaned_data["labels"])
            messages.success(request, _("task_edit"))  # и здесь
            return redirect(reverse_lazy("tasks:list"))
        labels = task.labels.all()
        return render(
            request,
            "tasks/edit.html",
            {"form": form, "task_id": task_id, "task": task, "labels": labels},
        )


class TaskFormDeleteView(LoginRequiredMixin, View):
    template_name = "tasks/delete.html"

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user != task.author:
            messages.error(request, _("remove_task_error"))
            return redirect(reverse_lazy("tasks:list"))
        return render(request, self.template_name, {"task": task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user != task.author:
            messages.error(request, _("remove_task_error"))
        else:
            task.delete()
            messages.success(request, _("task_remove"))
        return redirect(reverse_lazy("tasks:list"))


class TaskFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        labels = task.labels.all()
        return render(
            request,
            "tasks/view.html",
            {"task_id": task_id, "task": task, "labels": labels},
        )
