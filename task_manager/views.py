from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import Label, Task, Status
from django.http import Http404
from .forms import LabelForm
from .filters import TaskFilter
from django_filters.views import FilterView
from django.http import HttpResponse

class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'task_manager/task_list.html'
    context_object_name = 'tasks'

@login_required
def label_list(request):
    labels = Label.objects.all()
    return render(request, 'task_manager/label_list.html', {'labels': labels})

@login_required
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelForm()
    return render(request, 'task_manager/label_form.html', {'form': form})

@login_required
def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'task_manager/label_form.html', {'form': form})

@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if label.tasks.exists():
        # Метку нельзя удалить, если она связана с задачами
        return redirect('label_list')
    if request.method == 'POST':
        label.delete()
        return redirect('label_list')
    return render(request, 'task_manager/label_confirm_delete.html', {'label': label})

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'task_manager/status_confirm_delete.html'
    context_object_name = 'status'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.tasks.exists():
            raise ValidationError("Статус не может быть удален, так как связан с задачами.")
        return obj

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'task_manager/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_manager/status_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('status_list')

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'task_manager/status_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('status_list')

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'task_manager/status_confirm_delete.html'
    context_object_name = 'status'

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно удален!')
        return reverse_lazy('status_list')

# Представление для получения списка пользователей
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        users_list = [{'id': user.id, 'username': user.username} for user in users]
        return JsonResponse(users_list, safe=False)

def home(request):
    return render(request, 'task_manager/home.html')

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, 'Задача успешно создана!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_manager/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        raise Http404('Вы не можете редактировать эту задачу.')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_manager/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        raise Http404('Вы не можете удалить эту задачу.')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('task_list')

    return render(request, 'task_manager/task_confirm_delete.html', {'task': task})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_manager/task_detail.html', {'task': task})

def index(request):
    a = None
    a.hello()  # Ошибка, вызывающая исключение
    return HttpResponse("Hello, world!")
