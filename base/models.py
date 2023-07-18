from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from django_softdelete.models import SoftDeleteModel
from mdeditor.fields import MDTextField

from accounts.models import User


class Topic(SoftDeleteModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    # slug = models.SlugField(max_length=200,unique=True,blank=False,null=False)
    slug = AutoSlugField(populate_from=["name"])
    description = models.TextField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Room(SoftDeleteModel):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)

    name = models.CharField(max_length=200, blank=False, null=False)
    # slug = models.SlugField(max_length=200,unique=True,blank=False,null=False)
    slug = AutoSlugField(populate_from=["name"])
    description = models.TextField(null=True, blank=True)

    TYPES = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    type = models.TextField(null=False, choices=TYPES, default="public")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("room", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Message(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    parent = models.ForeignKey(
        'self',
        related_name='replies',
        related_query_name='message',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    body = models.TextField()
    body = MDTextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]
 

class ReactionType(models.Model):
    name = models.CharField(max_length=70,null=False,blank=False)
    
    def __str__(self):
        return f"{self.name}"

class Reaction(models.Model):
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)
    message =  models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reaction_type.name} to {self.user.username}'s message"


class RoomInvitation(models.Model):
    inviter_id = models.ForeignKey(
        User, related_name="inviter", on_delete=models.CASCADE
    )
    invitee_id = models.ForeignKey(
        User, related_name="invitee", on_delete=models.CASCADE
    )
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    token = models.CharField(max_length=100, null=False, blank=False)
    is_accepted = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.room_id} - {self.inviter_id}"
