from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<slug:slug>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<slug:slug>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/", views.activityPage, name="activity"),
    path("room/<int:pk>/toggle-join/", views.toggleJoinRoom, name="toggle-room-join"),
    path("room/<str:slug>/invite/", views.sendRoomInvite, name="invite-room"),
    path(
        "room/accept-invite/<str:token>/",
        views.acceptRoomInvite,
        name="accept-invite-room",
    ),
    path('message/<int:pk>/reaction',views.toggleMessageReaction,name='message-reaction'),

    path('message/<int:pk>/reply',views.addMessageReply,name='message-reply')
]
