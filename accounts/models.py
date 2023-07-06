from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django_softdelete.models import SoftDeleteModel


class User(SoftDeleteModel, AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=False)
    bio = models.TextField(null=True)

    avatar = models.URLField(
        max_length=200,
        default='https://avatars.dicebear.com/api/bottts/default.svg'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.username
