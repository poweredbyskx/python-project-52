from django.urls import path
from .views import MyLoginView, SignUpView, ProfileView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # Пользовательская вьюшка входа с кастомной формой
    path('login/', MyLoginView.as_view(), name='login'),
    # Выход
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
    # Регистрация нового пользователя
    path('signup/', SignUpView.as_view(), name='signup'),
    # Страница профиля
    path('profile/', ProfileView.as_view(), name='profile'),
]