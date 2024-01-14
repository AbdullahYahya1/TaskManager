# forms.py

from django.forms import ModelForm
from .models import *

class TaskForm(ModelForm):
    class Meta:
        model = DayTask
        fields = ['title', 'description','estimated_time']
        # or use '__all__' to include all fields
