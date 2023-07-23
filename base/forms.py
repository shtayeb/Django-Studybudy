from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from mdeditor.fields import MDTextFormField

from .models import Message, Room, RoomInvitation


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'members']


class MessageForm(ModelForm):
    body = MDTextFormField(label='')

    class Meta:
        model = Message
        fields = ['body']
        # exclude = ['user','room']