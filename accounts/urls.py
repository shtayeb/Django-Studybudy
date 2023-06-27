from django.urls import include, path

from . import views

urlpatterns = [
    # path('login/',views.loginPage,name="login"),
    # path('register/',views.registerPage,name="register"),
    # path('logout/',views.logoutUser,name="logout"),
    path("profile/<str:username>/", views.userProfile, name="user-profile"),
    path("update-user/", views.updateUser, name="update-user"),
    path("", include("allauth.urls")),
]
