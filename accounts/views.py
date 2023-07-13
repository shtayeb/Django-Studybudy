from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from base.models import Topic

from .forms import UserForm
from .models import User


@require_http_methods('POST')
def searchUser(request):
    email = request.POST.get("email")

    results = User.objects.filter(email__icontains=email)[:5]

    context = {'results':results}

    return render(request,'accounts/partials/user-list.html',context)

# {% form.field hx-post='/accounts/check_username' hx-trigger='keyup throttle:2s' hx-target="username-error" %}
# <div id="username-error"></div>
def checkUsername(request):
    username = request.POST.geT('username')

    if User.objects.filter(username=username).exists():
        return HttpResponse("<div style='color:red'>This username is not available</div>")
    else:
        return HttpResponse("<div style='color:green'>This username is available</div>")
        

def userProfile(request, username):
    user = User.objects.get(username=username)

    rooms = user.room_set.select_related("host", "topic").annotate(
        participants_count=Count("participants")
    )

    room_messages = user.message_set.prefetch_related("user", "room")

    topics = Topic.objects.annotate(rooms_count=Count("room"))[:5]

    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }

    return render(request, "accounts/profile.html", context)


@login_required(login_url="/accounts/login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.avatar = form.cleaned_data['avatar']
            form.save()

            return redirect("user-profile", username=user.username)

    context = {"form": form}
    return render(request, "accounts/update_user.html", context)
