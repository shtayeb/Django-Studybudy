
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RoomForm
from .models import Message, Room, Topic, User

# rooms = [
#     {'id':1, 'name':'Lets Learn Python'},
#     {'id':2, 'name':'Lets Learn Python'},
#     {'id':3, 'name':'Lets Learn Python'},
# ]



def home(request):
    q = request.GET.get('q')

    if (request.GET.get('q') == None):
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ).prefetch_related('host','topic').annotate(participants_count=Count('participants'))

    topics = Topic.objects.annotate(rooms_count=Count('room'))[0:5]

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).prefetch_related('user','room')

    context = {'rooms': rooms, 'topics': topics, 'room_messages': room_messages}

    return render(request, 'base/home.html', context)


def room(request, slug):
    # room = Room.objects.get(id=pk)
    room = get_object_or_404(
        Room.objects.prefetch_related(
            Prefetch('host')
        ),
        slug=slug
    )

    # my_object = get_object_or_404(Room.objects.prefetch_related(Prefetch('related_objects', queryset=RelatedModel.objects.select_related('other_model'))), pk=my_id)

    room_messages = room.message_set.select_related(
        'user'
    ).all()

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', slug=room.slug)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    
    return render(request, 'base/room.html', context)


@login_required(login_url='accounts/login')
def createRoom(request):
    form = RoomForm()
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

        # form = RoomForm(request.POST)

        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host=request.user

        #     room.save()

        #     return redirect('home')

    context = {'form': form, 'topics': topics}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='accounts/login')
def updateRoom(request, slug):
    # room = Room.objects.get(id=pk)
    room = get_object_or_404(Room,slug=slug)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='accounts/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here !!')

    if request.method == 'POST':
        room.delete()

        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='accounts/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here 33 !!')

    if request.method == 'POST':
        message.delete()

        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})



def topicsPage(request):
    q = request.GET.get('q')

    if (request.GET.get('q') == None):
        q = ''

    topics = Topic.objects.filter(name__icontains=q).annotate(rooms_count=Count('room'))
    
    context = {'topics': topics}
    
    return render(request, 'base/topics.html', context)


def activityPage(request):
    # q = request.GET.get('q')

    # if(request.GET.get('q') == None):
    #     q = ''
    # topics = Topic.objects.filter(name__icontains=q)
    # context = {'topics':topics}

    room_messages = Message.objects.prefetch_related('user','room')

    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)
