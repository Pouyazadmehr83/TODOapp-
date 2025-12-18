from django.urls import path

from .views import create_task, details, home_view

app_name = "todo"
urlpatterns = [
    path("", home_view, name="home"),
    path("details/<int:id>/", details, name="details"),
    path("create/", create_task, name="create"),
    path("details/<int:id>/edit",update,name="update")
    ]
