from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
# from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

types =('daytask', 'weeklytask' , 'monthlytask')
task_forms = {
        'daytask': DayTaskForm,
        'weeklytask': WeeklyTaskForm,
        'monthlytask': MonthlyTaskForm
    }
@csrf_exempt  # Temporarily disable CSRF for demonstration
def send_number(request):
    if request.method == "POST" and request.user.is_authenticated:
        task = None
        data = json.loads(request.body)
        pk = data.get('number',-1)
        task_type = data.get('task_type',-1)
        if task_type == types[0]:
            task = DayTask.objects.get(pk=pk)
        elif task_type == types[1]:
            task = WeeklyTask.objects.get(pk=pk)
        elif task_type == types[2]:
            task = MonthlyTask.objects.get(pk=pk)
        if  request.user != task.user:
            return JsonResponse({'status': 'error', 'message': 'you are not allowed'})
        task.is_finished =not task.is_finished
        task.save()   
        return JsonResponse({'status': 'success', 'number_received': pk})
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'})


@login_required(login_url='login_form')
def index(request):
    daytask = request.user.day_tasks.all()
    weeklytask = request.user.weekly_tasks.all()
    monthlytask = request.user.monthly_tasks.all()
    return render(request, 'taskapp/index.html', {
        'daytask': daytask,
        'weeklytask': weeklytask,
        'monthlytask': monthlytask})


def task(request,pk):
      return HttpResponse(f'{pk} {DayTask.objects.get(pk=pk).user}')
  
def daylytask(request):
    return render(request, 'taskapp/daylytask.html',{})

def login_form(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = (request.POST.get('username','none'))
        password = (request.POST.get('password','none'))

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            return render(request, 'taskapp/login_register_form.html', 
                          { 'login':True
                        ,'error': 'Invalid username or password.'})

    return render(request, 'taskapp/login_register_form.html', {'login':True})

def register_form(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'taskapp/login_register_form.html')

def add_task(request, task_type):    
    form = task_forms.get(task_type , None)
    if not form:
        return HttpResponse('not allowed')
    if request.method == 'POST':
        form = form(request.POST)        
        if form.is_valid():
            formres = form.save(commit=False)
            formres.user = request.user
            formres.save()
            return redirect('index') 
        else:
            messages.error(request,'not good')
    else:
        form = form()
    return render(request, 'taskapp/add_task.html' , {'form':form})
    
def logout_page(request):
    logout(request)
    return redirect('login_form')