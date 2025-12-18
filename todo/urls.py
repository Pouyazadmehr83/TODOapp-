from django.urls import path

from .views import (
    create_task,
    delete_task,
    details,
    home_view,
    mark_task_done,
    update_task,
)

app_name = "todo"

urlpatterns = [
    path("", home_view, name="home"),
    path("create/", create_task, name="create"),
    path("details/<int:id>/", details, name="details"),
    path("details/<int:id>/edit/", update_task, name="update"),
    path("details/<int:id>/delete/", delete_task, name="delete"),
    path("details/<int:id>/done/", mark_task_done, name="mark_done"),
]
