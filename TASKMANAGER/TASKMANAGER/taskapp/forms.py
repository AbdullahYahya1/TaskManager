from django.forms import ModelForm
from .models import *
class DayTaskForm(ModelForm):
    class Meta:
        model = DayTask
        fields = ['title', 'description','estimated_time']
        # or use '__all__' to include all fields
class WeeklyTaskForm(ModelForm):
    class Meta:
        model = WeeklyTask
        fields = ['title', 'description','estimated_time','day_of_week']
        # or use '__all__' to include all fields
class MonthlyTaskForm(ModelForm):
    class Meta:
        model = MonthlyTask
        fields = ['title', 'description','estimated_time','day_of_month']
        # or use '__all__' to include all fields
