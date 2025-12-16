from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def home_view(request):
    task= Task.objects.all().values()
    context = {
    'task': task
  }
    return render(request, "todo/home.html",context)

def details(request, id):
  task = Task.objects.get(id=id)
  context = {
    'task': task
  }
  return render(request, "todo/details.html",context)