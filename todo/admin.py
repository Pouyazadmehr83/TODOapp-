from django.contrib import admin
from todo.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "priority", "is_done", "created_at","due_date"]
    list_filter = ["priority", "is_done"]
    search_fields = ["title", "description"]

admin.site.register(Task, TaskAdmin)