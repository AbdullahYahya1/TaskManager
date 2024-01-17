from django.contrib import admin
from .models import * 
admin.site.register(DayTask)
admin.site.register(WeeklyTask)
admin.site.register(MonthlyTask)
admin.site.register(SharedUser)
admin.site.register(Room)