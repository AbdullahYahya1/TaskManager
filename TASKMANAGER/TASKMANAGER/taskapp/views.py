from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseForbidden
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
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room = Room.objects.create(name=room_name)
        room.users.add(request.user)
        return redirect('index')  # or wherever you want to redirect
    return render(request, 'taskapp/create_room.html')

def index(request):
    query = request.GET.get('search', '')
    room_id = request.GET.get('room_id')  # Get room_id from URL
    rooms = Room.objects.filter(users=request.user.id)
    if request.user.is_authenticated:
        if room_id:
            room = get_object_or_404(Room, pk=room_id, users=request.user)
        else:
            room = rooms.first()  # Default to the first room
        # Filter tasks based on the search query
        daytask = room.day_tasks.filter(title__icontains=query)
        weeklytask = room.weekly_tasks.filter(title__icontains=query)
        monthlytask = room.monthly_tasks.filter(title__icontains=query)
        return render(request, 'taskapp/index.html', {
            'daytask': daytask,
            'weeklytask': weeklytask,
            'monthlytask': monthlytask,
            'room': room,
            'rooms': rooms,
            'query': query , 
            'users': room.users.all(),
            
        })
    else:
        return render(request, 'taskapp/index.html')

def task(request,pk):
    task_type= request.GET.get('taskType',-1)
    if task_type == types[0]:
        task = DayTask.objects.get(pk=pk)
    elif task_type == types[1]:
        task = WeeklyTask.objects.get(pk=pk)
    elif task_type == types[2]:
        task = MonthlyTask.objects.get(pk=pk)
    
    return render(request, 'taskapp/task.html', {
        'task':task,
        'task_type': task_type
    })

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
                # Authenticate and login the user
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # Create a default room for the new user
                    default_room = Room.objects.create(name=f"{username}'s Room")
                    default_room.owner = user
                    default_room.users.add(user)
                    # Redirect to the index page or a welcome page
                    return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'taskapp/login_register_form.html')

@login_required(login_url='login_form')
def add_task(request, room_id, task_type):    
    room = get_object_or_404(Room, pk=room_id)
    if not room.users.filter(id=request.user.id).exists():
        return HttpResponseForbidden('You do not have permission to add tasks to this room.')
    form_class = task_forms.get(task_type)
    if form_class is None:
        return HttpResponse('Task type not allowed')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.room = room 
            task.user = request.user
            task.save()
            return redirect('index')  
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = form_class()
    
    return render(request, 'taskapp/add_task.html', {'form': form, 'room': room , 'task_type':task_type[0:task_type.find('task')]})


def delete_task(request, task_id , task_type):
    if task_type == types[0]:
        task = DayTask.objects.get(pk=task_id)
    elif task_type == types[1]:
        task = WeeklyTask.objects.get(pk=task_id)
    elif task_type == types[2]:
        task = MonthlyTask.objects.get(pk=task_id)
    else:
        return HttpResponse('failed to find task')
    task.delete()
    return redirect('index')

def edit_task(request, task_id  ,task_type):
    form_class = task_forms.get(task_type)
    task = None
    if task_type == types[0]:
        task = DayTask.objects.get(pk=task_id)
    elif task_type == types[1]:
        task = WeeklyTask.objects.get(pk=task_id)
    elif task_type == types[2]:
        task = MonthlyTask.objects.get(pk=task_id)
    else:
        return HttpResponse('failed to find task')
    if request.method == 'POST':
        form = form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = form_class(instance = task)
    return render(request, 'taskapp/edit_task.html', {'form': form, 'room': task.room})
def logout_page(request):
    logout(request)
    return redirect('login_form')

def share_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_to_share_with = User.objects.get(email=email)
            room.users.add(user_to_share_with)
        except User.DoesNotExist:
            pass
    # Render a form for sharing a room
    return render(request, 'taskapp/share_room.html', {'room': room})
