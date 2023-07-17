import factory
from factory.django import DjangoModelFactory
from .models import AuthUser

class UserFactory(DjangoModelFactory):

    username = factory.Sequence(lambda num: f'user{num}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.Sequence(lambda x: f'qwerty{x}')

    class Meta:
        model = AuthUser