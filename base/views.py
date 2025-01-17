from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


# rooms = [
#   {'id':1, 'name':"Verilog"},
#   {'id':2, 'name':"VHDL"},
#   {'id':3, 'name':"FPGA"}
# ]
def home(request):
  q = request.GET.get('q') if request.GET.get('q')!=None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) | Q(description__icontains=q)
    )
  topics = Topic.objects.all()[0:5]

  room_count = rooms.count()

  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

  context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}
  return render(request, 'base/home.html',context )

def room(request,id):
  room = Room.objects.get(id=id)
  room_messages = room.message_set.all()
  participants = room.participants.all()
  if request.method=='POST':
    message = Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('room', id = room.id)
  for participant in participants:
    print(participant.username)


  context = {'room':room, 'room_messages': room_messages,'participants':participants}
  return render(request, 'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
  form=RoomForm()
  topics = Topic.objects.all()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)

    Room.objects.create(
      host=request.user,
      topic=topic,
      name=request.POST.get('name'),
      description=request.POST.get('description')

    )
    return redirect('home')
  context={'form':form, 'topics': topics}
  return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,id):
  room = Room.objects.get(id=id)
  topics = Topic.objects.all()
  form = RoomForm(instance=room)
  if request.user!=room.host:
    return HttpResponse("You are not allowed here")
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)
    room.name = request.POST.get('name')
    room.topic = topic
    room.description = request.POST.get('description')
    room.save()
    return redirect('home')
  context ={'form': form, 'topics': topics}
  return render(request,'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, id):
  room = Room.objects.get(id=id)
  if request.user!=room.host:
    return HttpResponse("You are not allowed here")
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html',{'obj':room})

def loginPage(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username, password=password)

    except:
      messages.error(request, "User doesn't exist")

    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or password does not exist')

  context = {"page": page}
  return render(request, 'base/login_register.html', context)

def logoutUser(request):
  logout(request)
  return redirect("home")

def registerPage(request):
  form = UserCreationForm()
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request,"An error occured during registration")
  return render(request,'base/login_register.html', {'form':form})

@login_required(login_url='login')
def deleteMessage(request, id):
  message = Message.objects.get(id=id)
  if request.user!=message.user:
    return HttpResponse("You are not allowed here")
  if request.method == 'POST':
    message.delete()
    return redirect('home')
  return render(request, 'base/delete.html',{'obj':message})

def userProfile(request,id):
  user = User.objects.get(id=id)
  rooms = user.room_set.all()
  topics = Topic.objects.all()
  room_messages = user.message_set.all()
  context= {'user':user, 'rooms': rooms, 'room_messages': room_messages, 'topics':topics}
  return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
  user=request.user
  form=UserForm(instance=user)
  if request.method == 'POST':
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      return redirect('user-profile',id=user.id)
  context={'form':form}
  return render(request, 'base/update_user.html', context)

def topicsPage(request):
  q = request.GET.get('q') if request.GET.get('q')!= None else ''
  context = {}
  topics = Topic.objects.filter(name__icontains=q)
  context = {'topics':topics}
  return render(request, 'base/topics.html', context)

def activityPage(request):
  room_messages = Message.objects.all()
  context={'room_messages': room_messages}
  return render(request, 'base/activity.html', context)
