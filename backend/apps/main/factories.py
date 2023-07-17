import factory
from factory.django import DjangoModelFactory

from .base_models import *
from .models import *
from apps.  accounts.factories import UserFactory

class ActionFactory(DjangoModelFactory):

    text = factory.Faker('sentence', nb_words = 4)

    class Meta:
        model = BaseAction

class ContentFactory(DjangoModelFactory):

    name = factory.Faker('sentence', nb_words = 4)
    description = factory.Faker('paragraph', nb_sentences = 8)

    class Meta:
        model = BaseContent

class PersonFactory(DjangoModelFactory):

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date')

    class Meta:
        model = BasePerson

class AuthorFactory(PersonFactory):

    class Meta:
        model = Author

class CompanyFactory(ContentFactory):

    class Meta:
        model = Company

class ActorFactory(PersonFactory):

    class Meta:
        model = Actor

class CategoryFactory(DjangoModelFactory):

    name = factory.Faker('sentence', nb_words = 1)
    description = factory.Faker('paragraph', nb_sentences = 8)

    class Meta:
        model = Category

class MangaFactory(ContentFactory):

    class Meta:
        model = Manga

class AnimeFactory(ContentFactory):

    class Meta:
        model = Anime

class NewsFactory(ContentFactory):

    class Meta:
        model = News

class CommentFactory(ActionFactory):

    class Meta:
        model = Comment

class ReviewFactory(ActionFactory):
    
    class Meta:
        model = Review