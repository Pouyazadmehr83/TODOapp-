from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # انتخاب‌ها برای اولویت (ترتیب مهم است - اول تعریف شود)
    class PriorityChoices(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    # قابلیت جدید: نگه داشتن روز هفته به صورت جداگانه تا فیلترهای صفحه اصلی درست کار کنند
    class WeekDayChoices(models.IntegerChoices):
        SUNDAY = 1, "Sunday"
        MONDAY = 2, "Monday"
        TUESDAY = 3, "Tuesday"
        WEDNESDAY = 4, "Wednesday"
        THURSDAY = 5, "Thursday"
        FRIDAY = 6, "Friday"
        SATURDAY = 7, "Saturday"

    # فیلدهای مدل
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="user",
    )
    title = models.CharField(max_length=225, verbose_name="title")
    description = models.TextField(blank=True, verbose_name="description")
    is_done = models.BooleanField(default=False, verbose_name="is done")

    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        verbose_name="priority",
    )
    day_of_week = models.PositiveSmallIntegerField(
        choices=WeekDayChoices.choices,
        blank=True,
        null=True,
        verbose_name="day of week",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")
    due_date = models.DateTimeField(
        null=True, blank=True, verbose_name="due date"
    )  # متا دیتا

    class Meta:
        ordering = ["-created_at"]  # جدیدترین اول
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} - {self.user.username}"  # اینجا اصلاح شد

    # قابلیت جدید: تعیین رنگ کارت بر اساس اولویت برای UI
    @property
    def priority_color(self):
        color_map = {
            self.PriorityChoices.LOW: "success",
            self.PriorityChoices.MEDIUM: "warning",
            self.PriorityChoices.HIGH: "danger",
        }
        return color_map.get(self.priority, "secondary")
