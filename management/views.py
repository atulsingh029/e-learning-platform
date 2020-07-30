from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import authenticate
from .forms import CreateRoom
from custom_user.models import Room,Custom_User
import random

def dashboard(request):
    if request.user.is_authenticated:
        test=request.user
        return HttpResponse('<a href="/dashboard/addroom">add room </a>')

def addroom(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        room = Room()
        room.title = title
        room.description = description
        temp = User.objects.filter(username=str(request.user))
        temp = Custom_User.objects.filter(user = temp[0])
        room.organization = temp[0]
        room.room_number = random.randrange(0,9999999) # only for testing : reimplementation required
        room.save()
        return redirect('/dashboard')

    form = CreateRoom()
    return render(request,'dashboard/dashboard.html', context={'form':form})
