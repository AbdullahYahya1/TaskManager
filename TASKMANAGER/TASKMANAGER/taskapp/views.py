from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
# from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'taskapp/index.html', {})
def login_register_form(request):
    return render(request, 'taskapp/login_register_form.html', {'UserCreationForm':UserCreationForm})
