from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .models import Message, ReactionType, Room, RoomInvitation, Topic

admin.site.register(RoomInvitation)
admin.site.register(ReactionType)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "room",
        "created",
    )

    search_fields = ("user__username", "room__name")


admin.site.register(Message, MessageAdmin)


class MembersInline(admin.TabularInline):
    model = Room.members.through


class RoomAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name',)}
    list_display = ("id", "name", "host", "type")

    list_filter = ("type",)
    search_fields = ("host__username", "name")

    inlines = [
        MembersInline,
    ]


admin.site.register(Room, RoomAdmin)


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class TopicAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "github_url"]
    # prepopulated_fields = {'slug': ('name',)}
    search_fields = ("name",)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")[1:]
            print(csv_data)

            for x in csv_data:
                fields = x.split(",")
                Topic.objects.update_or_create(
                    name=fields[1],
                    description=fields[2],
                    github_url=fields[3],
                )

            url = reverse("admin:base_topic_changelist")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


admin.site.register(Topic, TopicAdmin)
