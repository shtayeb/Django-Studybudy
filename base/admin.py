from django.contrib import admin
from .models import Room, Topic, Message, User
from django import forms
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class ParticipantsInline(admin.TabularInline):
    model = Room.participants.through

class RoomAdmin(admin.ModelAdmin):
    inlines = [
        ParticipantsInline,
    ]

admin.site.register(Room,RoomAdmin)

# UserAdmin
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    
    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = User.objects.update_or_create(
                    first_name = fields[2],
                    last_name = fields[3],
                    username = fields[2]+'-'+get_random_string(length=5),
                    name = fields[2] + ' ' +fields[3],
                    email = fields[1],
                    avatar = fields[4],
                    password=make_password('12345678')
                    )
                    
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
                

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

admin.site.register(User,UserAdmin)

#End UserAdmin

admin.site.register(Topic)
admin.site.register(Message)
