from django.urls import include, path

from . import views

urlpatterns = [
    path("profile/<str:username>/", views.userProfile, name="user-public-profile"),
    path("update-user/", views.updateUser, name="update-user"),
    # Htmx urls
    path("search-user/", views.searchUser, name="search-user"),
    path("user/<str:username>/delete", views.deleteUser, name="delete-user"),
    # All Auth
    path("", include("allauth.urls")),
]
