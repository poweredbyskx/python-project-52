from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CustomUserCreationForm, CustomUserChangeForm
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, _("log_out"))
        return redirect('root')


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {
            'form': AuthenticationForm()
        })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, _("auth_success"))
                return redirect('root')

        messages.error(request, _("auth_form_error"))
        return render(request, 'registration/login.html', {'form': form})


class IndexView(View):
    def get(self, request):
        return render(request, 'welcome/index.html')


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/index.html', {'users': users})


class UsersFormCreateView(View):
    def get(self, request):
        return render(request, 'registration/register.html', {
            'form': CustomUserCreationForm()
        })

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("user_create_success"))
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})


class UsersFormEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if str(request.user.id) != str(pk):
            messages.error(request, _("edit_error"))
            return redirect('users')

        user = get_object_or_404(User, id=pk)
        form = CustomUserChangeForm(instance=user)
        return render(request, 'users/edit.html', {'form': form, 'user': user})

    def post(self, request, pk):
        if str(request.user.id) != str(pk):
            messages.error(request, _("edit_error"))
            return redirect('users')

        user = get_object_or_404(User, id=pk)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("edit_success"))
            return redirect('users')
        return render(request, 'users/edit.html', {'form': form, 'user': user})


class UsersFormDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        return render(request, 'users/delete.html', {'user': user, 'user_id': pk})

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if str(request.user.id) != str(pk):
            messages.error(request, _("delete_permission_error"))
            return redirect('users')

        has_tasks = Task.objects.filter(author_id=pk).exists() or Task.objects.filter(executor_id=pk).exists()
        if has_tasks:
            messages.error(request, _("remove_error"))
            return redirect('users')

        user.delete()
        messages.success(request, _("remove_success"))
        return redirect('users')
