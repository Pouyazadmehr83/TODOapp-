from django.urls import path
from .views import home_view,details

app_name = "todo"

urlpatterns = [
    path('', home_view, name="home"),
    path('details/<int:id>', views.details, name='details'),

]
