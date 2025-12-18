from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
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
    search_query = request.GET.get("q", "").strip()
    priority_filter = request.GET.get("priority", "")
    status_filter = request.GET.get("status", "")

    if search_query:
        # قابلیت جدید: جستجوی زنده بر اساس عنوان و توضیحات
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    if priority_filter in dict(Task.PriorityChoices.choices):
        # قابلیت جدید: فیلتر اولویت
        tasks = tasks.filter(priority=priority_filter)
    else:
        priority_filter = ""

    if status_filter in ["done", "pending"]:
        # قابلیت جدید: فیلتر وضعیت انجام شدن
        tasks = tasks.filter(is_done=(status_filter == "done"))
    else:
        status_filter = ""
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

    paginator = Paginator(tasks, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # جهت حفظ پارامترها در pagination و فیلتر روز
    query_params = request.GET.copy()
    dayless_query = query_params.copy()
    dayless_query.pop("day", None)
    dayless_query.pop("page", None)
    query_params.pop("page", None)
    base_query = query_params.urlencode()
    query_without_day = dayless_query.urlencode()

    context = {
        "tasks": page_obj.object_list,
        "page_obj": page_obj,
        "week_days": WEEK_DAYS,
        "selected_day": selected_day,
        "selected_day_label": selected_day_label,
        "search_query": search_query,
        "priority_filter": priority_filter,
        "status_filter": status_filter,
        "base_query": base_query,
        "query_without_day": query_without_day,
        "priority_choices": Task.PriorityChoices.choices,
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
