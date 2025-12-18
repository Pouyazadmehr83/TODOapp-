from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task

# توضیح: نگاشت روزهای هفته برای فیلتر کردن وظایف (با استفاده از فیلد جدید مدل)
WEEK_DAYS = list(Task.WeekDayChoices.choices)


@login_required
def home_view(request):
    # باگ: قبلاً همه‌ی تسک‌های کاربران نمایش داده می‌شد و داده‌ها افشا می‌شد.
    tasks = Task.objects.filter(user=request.user)
    day_param = request.GET.get("day")
    selected_day = None
    selected_day_label = None
    if day_param:
        try:
            selected_day = int(day_param)
        except (TypeError, ValueError):
            selected_day = None
        else:
            if selected_day in range(1, 8):
                # قابلیت جدید: فیلتر روزانه بر اساس فیلد day_of_week.
                tasks = tasks.filter(day_of_week=selected_day)
                selected_day_label = dict(WEEK_DAYS).get(selected_day)
            else:
                selected_day = None

    context = {
        "tasks": tasks,
        "week_days": WEEK_DAYS,
        "selected_day": selected_day,
        "selected_day_label": selected_day_label,
    }
    return render(request, "todo/home.html", context)


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
    return render(request, "todo/task_form.html", {"form": form, "action": "Create"})


@login_required
def update_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # قابلیت جدید: پیام موفقیت برای ویرایش.
            messages.success(request, "Task updated successfully.")
            return redirect("todo:details", id=task.id)
        messages.error(request, "Please fix the errors below.")
    else:
        form = TaskForm(instance=task)
    return render(request, "todo/task_form.html", {"form": form, "action": "Update"})


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == "POST":
        # قابلیت جدید: حذف امن تسک با تایید کاربر.
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect("todo:home")
    return redirect("todo:details", id=id)


@login_required
def mark_task_done(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == "POST":
        # قابلیت جدید: رادیو باتن وضعیت انجام تسک را true می‌کند.
        task.is_done = True
        task.save(update_fields=["is_done"])
        messages.success(request, "Task marked as done.")
    return redirect("todo:details", id=id)
