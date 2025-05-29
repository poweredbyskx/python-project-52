from django.urls import path
from task_manager.statuses import views
from task_manager.statuses.views import (
    StatusesFormCreateView,
    StatusFormEditView,
    StatusFormDeleteView,
)

app_name = "statuses"

urlpatterns = [
    path("", views.StatusesView.as_view(), name="list"),
    path(
        "create/",
        StatusesFormCreateView.as_view(),
        name="new_status",
    ),
    path(
        "<int:pk>/update/",
        StatusFormEditView.as_view(),
        name="edit_status",
    ),
    path(
        "<int:pk>/delete/",
        StatusFormDeleteView.as_view(),
        name="drop_status",
    ),
]
