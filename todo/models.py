from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # انتخاب‌ها برای اولویت (ترتیب مهم است - اول تعریف شود)
    class PriorityChoices(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
    
    # فیلدهای مدل
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='user'
    )
    title = models.CharField(max_length=225, verbose_name='title')
    description = models.TextField(blank=True, verbose_name='description')
    is_done = models.BooleanField(default=False, verbose_name='is done')
    
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        verbose_name='priority'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='due date')    # متا دیتا
    class Meta:
        ordering = ['-created_at']  # جدیدترین اول
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"  # اینجا اصلاح شد