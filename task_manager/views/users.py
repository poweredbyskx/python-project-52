from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages

class UserListView(ListView):
    model = User
    template_name = 'task_manager/users/index.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'task_manager/users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'task_manager/users/update.html'
    success_url = reverse_lazy('users_list')

    def test_func(self):
        return self.request.user == self.get_object()

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно обновлён')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'task_manager/users/delete.html'
    success_url = reverse_lazy('users_list')

    def test_func(self):
        return self.request.user == self.get_object()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Пользователь успешно удалён')
        return super().delete(request, *args, **kwargs)
