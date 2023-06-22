from django import forms
from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.crypto import get_random_string

from .models import User


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
                    
            url = reverse('admin:accounts_user_changelist')
            return HttpResponseRedirect(url)
                

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

admin.site.register(User,UserAdmin)
