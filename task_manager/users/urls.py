from django.urls import path
from task_manager.users.views import (
    UsersView,
    UsersFormCreateView,
    UsersFormEditView,
    UsersFormDeleteView,
)

app_name = "users"

urlpatterns = [
    path("", UsersView.as_view(), name="users"),
    path("create/", UsersFormCreateView.as_view(), name="new_user"),
    path("<int:pk>/update/", UsersFormEditView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UsersFormDeleteView.as_view(), name="user_delete"),
]
