from django.forms import ModelForm
from todo.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        # باگ: فیلدها خارج از Meta تعریف شده بودند و فرم هیچ مقداری را نمایش نمی‌داد.
        fields = ["title", "description", "due_date", "priority", "is_done"]
