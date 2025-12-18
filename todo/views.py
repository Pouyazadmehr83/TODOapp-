from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


@login_required
def home_view(request):
    # باگ: قبلاً همه‌ی تسک‌های کاربران نمایش داده می‌شد و داده‌ها افشا می‌شد.
    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo/home.html", {"tasks": tasks})


@login_required
def details(request, id):
    # باگ: جزئیات بدون بررسی مالکیت نمایش داده می‌شد.
    task = get_object_or_404(Task, id=id, user=request.user)
    return render(request, "todo/details.html", {"task": task})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # باگ: قبلاً به جای user فیلد اشتباه پر می‌شد و رکورد به کاربر وصل نمی‌شد.
            task.user = request.user
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect("todo:details", id=task.id)
        messages.error(request, "Please fix the errors below.")
    else:
        # باگ: فرم اشتباهی استفاده شده بود.
        form = TaskForm()
    return render(request, "todo/task_form.html", {"form": form})
