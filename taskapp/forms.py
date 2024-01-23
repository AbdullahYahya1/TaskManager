from django.forms import ModelForm, ChoiceField
from .models import *


class DayTaskForm(ModelForm):
    class Meta:
        model = DayTask
        fields = [
            "title",
            "description",
            "estimated_time",
        ]


class WeeklyTaskForm(ModelForm):
    class Meta:
        model = WeeklyTask
        fields = ["title", "description", "estimated_time", "day_of_week"]


class MonthlyTaskForm(ModelForm):
    day_of_month = ChoiceField(choices=[(day, day) for day in range(1, 32)])

    class Meta:
        model = MonthlyTask
        fields = ["title", "description", "estimated_time", "day_of_month"]
