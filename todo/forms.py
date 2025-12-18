from django import forms
from django.forms import ModelForm

from todo.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        # باگ: فیلدها خارج از Meta تعریف شده بودند و فرم هیچ مقداری را نمایش نمی‌داد.
        fields = [
            "title",
            "description",
            "due_date",
            "day_of_week",
            "priority",
            "is_done",
        ]
        # بهبود: ویجت‌ها اضافه شد تا فرم کاربرپسندتر و واضح‌تر شود.
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Task title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add some notes",
                    "rows": 4,
                }
            ),
            "due_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "day_of_week": forms.Select(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "is_done": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
