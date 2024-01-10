from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
# from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_form')
def index(request):
    daytask = request.user.day_tasks.all()
    weeklytask = request.user.weekly_tasks.all()
    monthlytask = request.user.monthly_tasks.all()
    return render(request, 'taskapp/index.html', {
        'daytask': daytask,
        'weeklytask': weeklytask,
        'monthlytask': monthlytask})



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

def logout_page(request):
    logout(request)
    return redirect('login_form')