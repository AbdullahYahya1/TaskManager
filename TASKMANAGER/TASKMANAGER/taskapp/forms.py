from django.forms import ModelForm, ChoiceField
from .models import *
class DayTaskForm(ModelForm):
    class Meta:
        model = DayTask
        fields = ['title', 'description','estimated_time',]
        # or use '__all__' to include all fields
class WeeklyTaskForm(ModelForm):
    day_of_week = ChoiceField(choices=[(day, day) for day in range(1, 8)])
    
    class Meta:
        model = WeeklyTask
        fields = ['title', 'description','estimated_time','day_of_week']
        # or use '__all__' to include all fields
class MonthlyTaskForm(ModelForm):
    day_of_month = ChoiceField(choices=[(day, day) for day in range(1, 32)])
    class Meta:
        model = MonthlyTask
        fields = ['title', 'description','estimated_time','day_of_month']
        # or use '__all__' to include all fields
