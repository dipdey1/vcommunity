from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def rooms(request,pk):
    room = Room.objects.get(id=pk)
    replies = room.replies_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        reply = Replies.objects.create(
            user = request.user.profile,
            room= room,
            body= request.POST.get('body')
        )
        room.participants.add(request.user.profile)
        return redirect('rooms', pk=room.id)

    context ={'room': room, 'messages': replies, 'participants': participants}
    return render(request, 'rooms/rooms.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_replies = Replies.objects.filter(Q(room__topic__name__icontains = q))
    context ={'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_replies}
    return render(request,'rooms/home.html', context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)
        Room.objects.create(
            host=request.user.profile,
            topic=topic,
            name= request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context ={'form': form, 'topics': topics}
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user.profile != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, 'Room was updated successfully!')
        return redirect('home')
    context ={'form': form, 'topics': topics, 'room': room}
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user.profile != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room was deleted successfully')
        return redirect('home')
    return render(request, 'rooms/delete.html', {'obj': room})

@login_required(login_url="login")
def deleteReply(request, pk):
    reply = Replies.objects.get(id=pk)

    if request.user.profile != reply.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply was deleted successfully')
        return redirect('home')
    return render(request, 'rooms/delete.html', {'obj': reply})


def userProfile(request, pk):
    user = Profile.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.replies_set.all()
    topics = Topic.objects.all()
    context ={'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'rooms/profile.html', context)