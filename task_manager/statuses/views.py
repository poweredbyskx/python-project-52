from django.shortcuts import render, redirect
from django.views import View
from .forms import StatusCreationForm
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.mixins import DeleteView, EditView, FormView


class StatusViewForm:
    value = Status
    template = "index.html"


class StatusesView(LoginRequiredMixin, View, StatusViewForm, FormView):
    pass


class StatusesFormCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "new.html",
                      {"form": StatusCreationForm()})

    def post(self, request):
        form = StatusCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, gettext("status_created"))
            return redirect("statuses:list")
        return render(request, "new.html", {"form": form})


class StatusEditForm:
    value = Status
    template = "edit.html"
    form = StatusCreationForm
    text = "status_edit"
    path = "statuses:list"


class StatusFormEditView(LoginRequiredMixin, View, StatusEditForm, EditView):
    def get(self, request, *args, **kwargs):
        status = Status.objects.get(id=kwargs.get("pk"))
        form = StatusCreationForm(instance=status)
        context = {"form": form, "status_id": status.id}
        return render(request, "edit.html", context)

    def post(self, request, *args, **kwargs):
        status = Status.objects.get(id=kwargs.get("pk"))
        form = StatusCreationForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, gettext("Статус успешно изменен"))
            return redirect("statuses:list")
        context = {"form": form, "status_id": status.id}
        return render(request, "edit.html", context)


class StatusForm:
    value = Status
    template = "delete.html"


class StatusFormDeleteView(LoginRequiredMixin, View, StatusForm, DeleteView):
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("pk")
        status = Status.objects.get(id=status_id)
        if Task.objects.filter(status_id=status_id).exists():
            messages.error(request, gettext("status_error"))
            return redirect("statuses:list")
        status.delete()
        messages.success(request, gettext("status_remove"))
        return redirect("statuses:list")
