from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Room, RoomInvitation


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


