from django.urls import path
from task_manager.tasks.views import (
    TasksView,
    TaskFormCreateView,
    TaskFormEditView,
    TaskFormDeleteView,
    TaskFormView,
)

app_name = "tasks"

urlpatterns = [
    path("", TasksView.as_view(), name="list"),
    path("create/", TaskFormCreateView.as_view(), name="create"),
    path("<int:pk>/update/", TaskFormEditView.as_view(), name="edit_task"),
    path("<int:pk>/delete/", TaskFormDeleteView.as_view(), name="drop_task"),
    path("<int:pk>/", TaskFormView.as_view(), name="view_task"),
]
