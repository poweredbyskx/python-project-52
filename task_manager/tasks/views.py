from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from task_manager.mixins import EditView
from .forms import TaskCreationForm, TaskFilter
from task_manager.tasks.models import Task
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.shortcuts import get_object_or_404


class TasksView(LoginRequiredMixin, FilterView):
    def get(self, request, *args, **kwargs):
        is_creator = False
        labels = request.GET.getlist('labels')
        status_id = request.GET.get('status', '')
        executor = request.GET.get('executor', '')
        if request.GET.get('only_own_tasks'):
            tasks = TaskFilter(request.GET, queryset=Task.objects.filter(author_id=request.user.id))
            is_creator = True
        else:
            tasks = TaskFilter(request.GET, queryset=Task.objects.all())
        return render(request, 'tasks/task_filter.html',
                      {
                          'filter': tasks,
                          'is_creator': is_creator,
                          'labels': labels,
                          'status_id': status_id,
                          'executor': executor
                      })

class TaskFormCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {'form': TaskCreationForm()}
        return render(request, 'tasks/new.html', context)

    def post(self, request):
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            for label in form.cleaned_data['labels']:
                task.labels.add(label)
            task.save()
            messages.success(request, gettext("task_created"))
            return redirect(reverse_lazy('tasks:list'))
        return render(request, 'tasks/new.html', {'form': form})

class TaskForm:
    value = Task
    template = 'tasks/edit.html'
    form = TaskCreationForm
    text = 'task_edit'
    path = 'tasks'


class TaskFormEditView(LoginRequiredMixin, View, TaskForm, EditView):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        labels = task.labels.all().values_list('name')
        form = TaskCreationForm(instance=task)
        return render(request, 'tasks/edit.html',
                      {'form': form, 'task_id': task_id, 'task': task,
                       'labels': labels})
    pass


class TaskFormDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        return render(request, 'tasks/delete.html', {'task': task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        if request.user != task.author:
            messages.error(request, gettext("remove_task_error"))
            return redirect(reverse_lazy('tasks:list'))
        task.delete()
        messages.success(request, gettext("task_remove"))
        return redirect(reverse_lazy('tasks:list'))


class TaskFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        labels = task.labels.all()
        return render(request, 'tasks/view.html',
                      {'task_id': task_id, 'task': task, 'labels': labels})
