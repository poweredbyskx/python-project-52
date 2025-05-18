from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm, CustomUserChangeForm
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.contrib import messages
from django.utils.translation import gettext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.INFO,
                             gettext("log_out"))
        return redirect('root')


class LoginView(View):
    def get(self, request):
        context = {
            'form': AuthenticationForm()
        }
        return render(request, 'registration/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request.POST)
        context = {
            'form': form
        }
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 gettext("auth_success"))
            return redirect('root')
        else:
            messages.error(request, gettext("auth_form_error"))
            return render(request, 'registration/login.html', context)


class IndexView(View):
    def get(self, request):
        return render(request, 'welcome/index.html')


class UsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/index.html', context={'users': users})


class UsersFormCreateView(View):
    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("✅ Форма валидна")
            print("🧍 Новый пользователь:", form.cleaned_data)
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 gettext("user_create_success"))
            return redirect('login')
        else:
            print("❌ Ошибки формы:")
            print(form.errors)

        context = {
            'form': form
        }
        return render(request, 'registration/register.html', context)


class UsersFormEditView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext("auth_error"))
            return redirect('login')
        if request.user.id != kwargs.get('pk'):
            messages.error(request, gettext("edit_error"))
            return redirect('users')
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        user_form = CustomUserChangeForm(instance=user)
        return render(request, 'users/edit.html', {'form': user_form, 'user': user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            messages.success(request, gettext("edit_success"))
            return redirect('users')
        return render(request, 'users/edit.html', {'form': user_form, 'user': user})


class UsersFormDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        return render(request, 'users/delete.html',
                      {'user': user, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        author = Task.objects.filter(author_id=user_id)
        executor = Task.objects.filter(executor_id=user_id)
        if author or executor:
            messages.add_message(request, messages.ERROR,
                                 gettext("remove_error"))
            return redirect('users')
        if user:
            user.delete()
            messages.add_message(request, messages.SUCCESS,
                                 gettext("remove_success"))
            return redirect('users')
