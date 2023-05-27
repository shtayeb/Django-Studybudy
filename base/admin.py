from django.contrib import admin
from .models import Room, Topic, Message, User

class ParticipantsInline(admin.TabularInline):
    model = Room.participants.through

class RoomAdmin(admin.ModelAdmin):
    inlines = [
        ParticipantsInline,
    ]

admin.site.register(Room,RoomAdmin)


admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
