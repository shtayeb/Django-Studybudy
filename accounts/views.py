from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.shortcuts import redirect, render

from base.models import Topic

from .forms import MyUserCreationForm, UserForm
from .models import User

# def logoutUser(request):
#     logout(request)
#     return redirect('home')


# def registerPage(request):
#     form = MyUserCreationForm()

#     if request.method == 'POST':
#         form = MyUserCreationForm(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()

#             user.save()

#             # from django auth
#             login(request, user)

#             return redirect('home')
#         else:
#             messages.error(request, 'An error has occured. Try again !')

#     context = {'form': form}
#     return render(request, 'accounts/login_register.html', context)


# def loginPage(request):
#     page = "login"

#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         email = request.POST.get('email').lower()
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(email=email)
#         except:
#             messages.error(request, 'User does not exist')

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Email or password does not exist')

#     context = {'page': page}
#     return render(request, 'accounts/login_register.html', context)


def userProfile(request, username):
    user = User.objects.get(username=username)

    rooms = user.room_set.select_related("host", "topic").annotate(
        participants_count=Count("participants")
    )

    room_messages = user.message_set.prefetch_related("user", "room")

    topics = Topic.objects.annotate(rooms_count=Count("room"))

    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }

    return render(request, "accounts/profile.html", context)


@login_required(login_url="accounts/login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

            return redirect("user-profile", username=user.username)

    context = {"form": form}
    return render(request, "accounts/update_user.html", context)
