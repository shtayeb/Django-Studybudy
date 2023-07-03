
from random import randint

import factory
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from factory.faker import faker

from .models import User

FAKE = faker.Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = 1
    is_superuser = 0
    is_staff = 0
    password = make_password('12345678')

    @factory.lazy_attribute
    def bio(self):
        x = ""
        for _ in range(0,5):
            x += "\n" + FAKE.paragraph(nb_sentences=2) + "\n"
        return x

    @factory.lazy_attribute
    def username(self):
        return f"{self.first_name}_{self.last_name}_{randint(1,11)}"
    
    @factory.lazy_attribute
    def email(self):
        return f"{self.username}@gmail.com"
    
    @factory.lazy_attribute
    def name(self):
        return f"{self.first_name} {self.last_name}"
