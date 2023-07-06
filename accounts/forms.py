# from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.forms import ModelForm

from .models import User


class MyUserCreationForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyUserCreationForm, self).save(request)

        # Add your own processing here.
        user.avatar = 'https://avatars.dicebear.com/api/bottts/' + user.username + '.svg'

        user.save()

        # You must return the original result.
        return user
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
