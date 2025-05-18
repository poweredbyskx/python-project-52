from django.urls import path
from .views import MyLoginView, SignUpView, ProfileView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]