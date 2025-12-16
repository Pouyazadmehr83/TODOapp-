from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='کاربر'
    )
    class PriorityChoices(models.TextChoices):
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'

    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        verbose_name='اولویت'
    )
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    id_done= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #priority = models.Choices()
     
    def __str__(self):
        return self.name

 