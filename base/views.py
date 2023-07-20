import datetime
import json

import jwt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Prefetch, Q, When
from django.http import HttpResponse, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from .forms import MessageForm, RoomForm
from .models import Membership, Message, ReactionType, Room, RoomInvitation, Topic, User

expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

SECRET_KEY = "secret_key_001"


@require_http_methods("POST")
@login_required(login_url="/accounts/login")
def addMessageReply(request, pk):
    # Get the room as well and check if the room is not archived
    message = Message.objects.get(pk=pk)
    # do dome error handling
    body = request.POST.get("body")
    user_id = request.user.id
    room_id = request.POST.get("room_id")

    reply = Message.objects.create(
        room_id=room_id, user_id=user_id, parent_id=message.id, body=body
    )
    # messages.success(request, "Reply Added Successfully !")

    reaction_types = ReactionType.objects.all()

    context = {"reply": reply, "reaction_types": reaction_types}
    return render(request, "base/_reply.html", context)


@login_required(login_url="/accounts/login")
@require_http_methods("POST")
def toggleMessageReaction(request, pk):
    if not request.user.is_authenticated:
        next_url = request.htmx.current_url_abs_path or ""
        return HttpResponseClientRedirect(f"/accounts/login/?next={next_url}")

    data = {"operation": ""}
    if request.method == "POST":
        message = Message.objects.get(pk=pk)
        reaction_type_id = json.loads(request.body)["reaction_type_id"]
        user = request.user

        # Check if the reaction exists
        msg_reaction = message.reaction_set.filter(
            user_id=user.id, message_id=message.id, reaction_type_id=reaction_type_id
        )

        if msg_reaction.exists():
            # remove the reaction
            msg_reaction.delete()
            data["operation"] = "removed"
        else:
            # add the reaction
            message.reaction_set.create(
                message_id=message.id,
                reaction_type_id=reaction_type_id,
                user_id=user.id,
            )
            data["operation"] = "added"
    else:
        messages.error(request, "GET request is not supported for this route !!")

    return JsonResponse(data, safe=False)


def toggleJoinRoom(request, pk):
    if not request.user.is_authenticated:
        next_url = request.htmx.current_url_abs_path or ""
        return HttpResponseClientRedirect(f"/accounts/login/?next={next_url}")

    # room = Room.objects.get(pk=pk)
    room = get_object_or_404(Room, pk=pk)

    template_name = "base/partials/room_join_toggle.html"

    if request.user.id == room.host_id:
        messages.error(request, "You are the room's host !!")

    is_joined = room.members.contains(request.user)

    if is_joined:
        room.members.remove(request.user)
        messages.success(request, "You left the room !")

    else:
        room.members.add(request.user)
        messages.success(request, "You joined the room !")

    # is_joined is old, so in the template I have used the negation of the variable
    context = {"is_joined": is_joined}

    return render(request, template_name, context)


@login_required(login_url="/accounts/login")
def sendRoomInvite(request, slug):
    # room = Room.objects.get(pk=pk)
    room = get_object_or_404(Room, slug=slug)

    if request.method == "POST":
        user_email = request.POST.get("email")

        if not user_email:
            raise ValidationError("The Email Address is required !!")

        invitee = get_object_or_404(User, email=user_email)
        # invitee = User.objects.get(email=user_email)

        # Check if there already exist an invite for the user
        # invitee_id, room_id
        # old_invitation = RoomInvitation.objects.get(room=room, invitee=invitee)
        old_invitation = RoomInvitation.objects.filter(room=room, invitee=invitee)

        if old_invitation.exists():
            old_invitation.delete()

        # encode room_id and invitee_id in the token
        # TODO : make the SECRET_KEY a secret in the .env file
        token = jwt.encode(
            {
                "room_id": room.id,
                "invitee_id": invitee.id,
                "exp": expiry_time,
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        invitation = RoomInvitation.objects.create(
            inviter_id=request.user.id,
            invitee_id=invitee.id,
            room_id=room.id,
            token=token,
            is_accepted=False,
        )

        # send email to the user
        template_name = "base/email/room_invitation_email.html"

        subject = "You have been invited to join a room"
        from_email = "shtb@shaharyartayeb.com"
        recipient_list = [user_email]

        invite_url = reverse("accept-invite-room", args=[token])
        invite_url = request.build_absolute_uri(invite_url)

        context = {
            "room_name": room.name,
            "user_email": user_email,
            "inviter": request.user,
            "invite_url": invite_url,
        }

        message = render_to_string(template_name, context)
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = "html"
        email.send()

        messages.success(request, "User has been invited to the room.")

        return redirect("room", room.slug)

    context = {"room": room}

    return render(request, "base/invite_user_form.html", context)


@login_required(login_url="/accounts/login")
def acceptRoomInvite(request, token):
    # decode the token
    try:
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=["HS256"], verify_expiration=True
        )
    except jwt.ExpiredSignatureError:
        # Token has expired
        messages.error(request, "The token has expired.")
        return redirect(request.META.get("HTTP_REFERER"))

    # get room_id and invitee_id from the token
    room_id = decoded_token["room_id"]
    invitee_id = decoded_token["invitee_id"]

    # Add the user to the room members
    room = get_object_or_404(Room, pk=room_id)
    invitee = get_object_or_404(User, pk=invitee_id)

    room.members.add(invitee)

    # update the invitation
    room_invitation = RoomInvitation.objects.get(token=token)
    room_invitation.is_accepted = True
    room_invitation.save()

    messages.success(request, "User has have been added to the room.")
    return redirect("room", slug=room.slug)


def home(request):
    q = request.GET.get("q")
    template_name = "base/home.html"

    if request.GET.get("q") == None:
        q = ""

    rooms = (
        Room.objects.filter(
            (
                Q(topic__name__icontains=q)
                | Q(name__icontains=q)
                | Q(description__icontains=q)
            )
            & ~Q(type="private")
            | Q(host_id=request.user.id)
        )
        .prefetch_related("host", "topic")
        .annotate(members_count=Count("members"))
    )

    if request.user.is_authenticated:
        # joined_private_rooms = request.user.membership_set.filter(Q(room__type="private"))
        joined_private_rooms = Room.objects.filter(type="private", members=request.user)
        rooms = rooms | joined_private_rooms

    topics = Topic.objects.annotate(rooms_count=Count("room"))[0:5]

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q),
        Q(room__is_deleted=False),
    ).exclude(room__type="private")

    if request.user.is_authenticated:
        room_messages = room_messages.filter(
            room__members=request.user
        ).prefetch_related("user", "room")[:10]

    page_number = request.GET.get("page", 1)
    paginator = Paginator(rooms, 20)  # Show 25 rooms per page.
    page_obj = paginator.get_page(page_number)

    try:
        rooms = paginator.page(page_number)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    if request.htmx:
        # htmx template
        template_name = "base/feed_component.html"

    context = {
        # "rooms": rooms,
        "page_obj": page_obj,
        "topics": topics,
        "room_messages": room_messages,
    }

    return render(request, template_name, context)


@login_required(login_url="/accounts/login")
@require_http_methods("POST")
def addMessage(request, room_id):
    if not request.user.is_authenticated:
        next_url = request.htmx.current_url_abs_path or ""
        return HttpResponseClientRedirect(f"/accounts/login/?next={next_url}")

    room = get_object_or_404(Room, pk=room_id)

    msg_form = MessageForm(request.POST)

    # if request.htmx:

    if msg_form.is_valid():
        message = msg_form.save(commit=False)
        message.user = request.user
        message.room = room

        message.save()

        room.members.add(request.user)

    reaction_types = ReactionType.objects.all()

    context = {"message": message, "reaction_types": reaction_types}
    return render(request, "base/_message.html", context)


def room(request, slug):
    fire_count = Count("reaction", filter=Q(reaction__reaction_type__name="🔥"))
    like_count = Count("reaction", filter=Q(reaction__reaction_type__name="👍"))
    poop_count = Count("reaction", filter=Q(reaction__reaction_type__name="💩"))

    room = get_object_or_404(
        Room.objects.prefetch_related(
            Prefetch(
                "message_set",
                Message.objects.filter(parent=None)
                .annotate(
                    fire_count=fire_count, like_count=like_count, poop_count=poop_count
                )
                .prefetch_related(
                    Prefetch(
                        "replies",
                        Message.objects.select_related("user").annotate(
                            fire_count=fire_count,
                            like_count=like_count,
                            poop_count=poop_count,
                        ),
                    ),
                    "user",
                ),
            ),
            Prefetch(
                "membership_set",
                Membership.objects.select_related("user")
                .filter(created__gte=datetime.date.today() - datetime.timedelta(days=7))
                .order_by("created"),
            ),
        ).select_related("host"),
        slug=slug,
    )

    is_joined = False

    # TODO : Move this to a directive
    if request.user.is_authenticated:
        is_joined = room.members.contains(request.user)

        if (
            not (room.host_id == request.user.id)
            and room.type == "private"
            and (not room.members.contains(request.user))
        ):
            messages.warning(request, "That room is private !")
            return redirect("home")

    msg_form = MessageForm()
    reply_form = MessageForm()

    reaction_types = ReactionType.objects.all()

    context = {
        "room": room,
        "msg_form": msg_form,
        "reply_form": reply_form,
        "is_joined": is_joined,
        "reaction_types": reaction_types,
    }

    return render(request, "base/room.html", context)

def settingsRoom(request, slug):
    room = get_object_or_404(Room,slug=slug)

    context = {
        "room": room,
    }

    return render(request, "base/room_settings.html", context)

@login_required(login_url="/accounts/login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            type=request.POST.get("type"),
        )
        return redirect("home")

        # form = RoomForm(request.POST)

        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host=request.user

        #     room.save()

        #     return redirect('home')

    context = {"form": form, "topics": topics}

    return render(request, "base/create_room.html", context)

@login_required(login_url="/accounts/login")
def updateRoom(request, slug):
    # room = Room.objects.get(id=pk)
    room = get_object_or_404(Room, slug=slug)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.type = request.POST.get("type")
        room.save()

        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/update_room.html", context)


@login_required(login_url="/accounts/login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!")

    if request.method == "POST":
        room.delete()

        return redirect("home")

    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="/accounts/login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here 33 !!")

    if request.method == "POST":
        message.delete()

        return redirect("room", message.room.slug)

    return render(request, "base/delete.html", {"obj": message})


@require_http_methods("POST")
def searchTopic(request):
    q = request.POST.get("q")

    if request.POST.get("q") == None:
        q = ""

    topics = Topic.objects.filter(name__icontains=q).annotate(
        rooms_count=Count("room")
    )[:10]

    context = {"topics": topics}

    return render(request, "base/partials/topic_list.html", context)


def topicsPage(request):
    q = request.GET.get("q")

    if request.GET.get("q") == None:
        q = ""

    topics = Topic.objects.filter(name__icontains=q).annotate(rooms_count=Count("room"))

    context = {"topics": topics}

    return render(request, "base/topics.html", context)


def activityPage(request):
    # q = request.GET.get('q')

    # if(request.GET.get('q') == None):
    #     q = ''
    # topics = Topic.objects.filter(name__icontains=q)
    # context = {'topics':topics}

    room_messages = Message.objects.prefetch_related("user", "room")

    context = {"room_messages": room_messages}
    return render(request, "base/activity.html", context)
