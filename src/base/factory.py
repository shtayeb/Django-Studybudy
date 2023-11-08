import factory
from factory.django import DjangoModelFactory
from factory.faker import faker

from accounts.factory import UserFactory
from accounts.models import User

from .models import Membership, Message, ReactionType, Room, Topic

FAKE = faker.Faker()


class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Faker("sentence", nb_words=4)
    slug = factory.Faker("slug")
    description = factory.Faker("sentence", nb_words=12)


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    host = factory.SubFactory(UserFactory)
    topic = factory.SubFactory(TopicFactory)

    name = factory.Faker("sentence", nb_words=4)
    type = factory.Iterator(Room.TYPES, getter=lambda c: c[0])

    @factory.lazy_attribute
    def description(self):
        x = ""
        for _ in range(0, 5):
            x += "\n" + FAKE.paragraph(nb_sentences=5) + "\n"
        return x

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.members.add(user)

        users = User.objects.all()[:5]

        membership = Membership.objects.create(room=self, user=self.host, is_admin=True)
        self.membership_set.add(membership)

        for user in users:
            self.members.add(user)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    user = factory.SubFactory(UserFactory)
    room = factory.SubFactory(RoomFactory)

    @factory.lazy_attribute
    def body(self):
        x = ""
        for _ in range(0, 5):
            x += "\n" + FAKE.posts(nb_sentences=5) + "\n"
        return x


REACTIONS = [
    ("👍", "like"),
    ("👎", "dislike"),
    ("💩", "poop"),
    ("🔥", "fire"),
]


class ReactionTypeFactory(DjangoModelFactory):
    class Meta:
        model = ReactionType

    name = factory.Iterator(REACTIONS, getter=lambda c: c[0])
