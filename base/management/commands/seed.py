from django.core.management.base import BaseCommand
from halo import Halo

from accounts.factory import UserFactory
from base.factory import ReactionTypeFactory, RoomFactory, TopicFactory


class Command(BaseCommand):
    help = "Generate fake data and seed the models with them, default are 10"

    def add_arguments(self, parser):
        # https://docs.python.org/3/library/argparse.html#the-add-argument-method
        # Optional!
        parser.add_argument("--amount", type=int, help="The amount of fake data you want")
        # parser.add_argument('amount', nargs='+', type=int)

    def _generate_data(self, amount):
        UserFactory.create_batch(amount)
        TopicFactory.create_batch(amount)
        RoomFactory.create_batch(amount)
        ReactionTypeFactory.create_batch(4)

    @Halo(text="Generating...", spinner="dots", color="blue", text_color="blue")
    def handle(self, *args, **options):
        amount = options.get("amount") or 10
        self._generate_data(amount)
