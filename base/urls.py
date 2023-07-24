from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Room
    path("room/create/", views.createRoom, name="create-room"),
    path(
        "room/<int:room>/search-member",
        views.searchMember,
        name="room-member-search",
    ),
    path("room/<slug:slug>/", views.room, name="room"),
    path("room/<int:pk>/toggle-join/", views.toggleJoinRoom, name="toggle-room-join"),
    path(
        "room/<slug:slug>/toggle-archived/",
        views.toggleRoomArchive,
        name="toggle-room-archived",
    ),
    path("room/<slug:slug>/invite/", views.sendRoomInvite, name="invite-room"),
    path("room/<slug:slug>/update", views.updateRoom, name="update-room"),
    path("room/<int:pk>/delete", views.deleteRoom, name="delete-room"),
    path(
        "room/accept-invite/<str:token>/",
        views.acceptRoomInvite,
        name="accept-invite-room",
    ),
    path("room/<slug:slug>/settings", views.settingsRoom, name="room-settings"),
    path("room/<slug:slug>/members", views.roomMembers, name="room-members"),
    # Room Membership
    path("membership/<int:pk>/delete", views.deleteMember, name="delete-member"),
    path(
        "membership/<int:pk>/toggle-admin",
        views.toggleRoomAdmin,
        name="room-toggle-admin",
    ),
    path(
        "membership/<int:pk>/toggle-blocked",
        views.toggleRoomMemberBlock,
        name="room-toggle-blocked",
    ),
    # RoomInvitation
    path("room/<slug:slug>/invitations", views.roomInvitation, name="room-invitations"),
    path(
        "room_invitation/<int:pk>/delete",
        views.roomInvitationDelete,
        name="delete-invitation",
    ),
    # Message
    path("room/<int:room_id>/add-message", views.addMessage, name="room-add-message"),
    path(
        "message/<int:pk>/reaction",
        views.toggleMessageReaction,
        name="message-reaction",
    ),
    path("message/<int:pk>/delete", views.deleteMessage, name="delete-message"),
    path("message/<int:pk>/reply", views.addMessageReply, name="message-reply"),
    path("message/<int:pk>/", views.showMessage, name="message-show"),
    # Topic
    path("topics/", views.topicsPage, name="topics"),
    path("topics/search-topic", views.searchTopic, name="search-topic"),
    #
    path("activity/", views.activityPage, name="activity"),
]
