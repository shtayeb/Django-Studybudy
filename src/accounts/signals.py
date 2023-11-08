from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import Room

from .models import User


@receiver(post_save, sender=User)
def post_save_user(sender, instance, **kwargs):
    print(instance.id)

    room = Room.objects.get_or_create(
        name="News",
        description="Webiste's news room.",
        host_id=1,
        topic_id=1,
    )[0]
    room.members.add(instance)
