from django.urls import path
from your_app.views import MyLoginView
from task_manager.users.views import (
    UsersView,
    UsersFormCreateView,
    UsersFormEditView,
    UsersFormDeleteView,
)

app_name = 'users'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('', UsersView.as_view(), name='users'),
    path('create/', UsersFormCreateView.as_view(), name='new_user'),
    path('<int:pk>/update/', UsersFormEditView.as_view(), name='patch_user'),
    path('<int:pk>/delete/', UsersFormDeleteView.as_view(), name='drop_user'),
]
