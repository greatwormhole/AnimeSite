import random

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.main.factories import *
from apps.accounts.factories import UserFactory

NUM_PERSON = 50
NUM_CONTENT = 50
ACTION_MULTIPLIER = 5
PERSONS_PER_CONTENT = 5
CATEGORIES_PER_CONTENT = 3
CATEGORIES = 10

class Command(BaseCommand):

    help = 'Generates fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write('Creating new data...')

        authors = [AuthorFactory() for _ in range(NUM_PERSON)]
        actors = [ActorFactory() for _ in range(NUM_PERSON)]

        categories = [CategoryFactory() for _ in range(CATEGORIES)]
        companies = [CompanyFactory() for _ in range(NUM_CONTENT)]
        mangas = [MangaFactory(
            author = random.choice(authors),
            company = random.choice(companies),
        ) for _ in range(NUM_CONTENT)]
        animes = [AnimeFactory(
            author = random.choice(authors),
            company = random.choice(companies),
            original = random.choice(mangas),
        ) for _ in range(NUM_CONTENT)]

        for manga in mangas:
            manga.categories.set(random.choices(categories, k=CATEGORIES_PER_CONTENT))
        
        for anime in animes:
            anime.categories.set(random.choices(categories, k=CATEGORIES_PER_CONTENT))
            anime.actors.set(random.choices(actors, k=PERSONS_PER_CONTENT))

        users = [UserFactory() for _ in range(NUM_PERSON)]

        comments_for_manga = [MangaCommentFactory(
            user = Profile.objects.get(user=random.choice(users)),
            manga = random.choice(mangas),
        ) for _ in range(round(NUM_PERSON * ACTION_MULTIPLIER))]
        comments_for_anime = [AnimeCommentFactory(
            user = Profile.objects.get(user=random.choice(users)),
            anime = random.choice(animes),
        ) for _ in range(round(NUM_PERSON * ACTION_MULTIPLIER))]
        reviews_for_manga = [MangaReviewFactory(
            user = Profile.objects.get(user=random.choice(users)),
            manga = random.choice(mangas),
            rate = random.randint(0, 10),
        ) for _ in range(round(NUM_PERSON * ACTION_MULTIPLIER))]
        reviews_for_anime = [AnimeReviewFactory(
            user = Profile.objects.get(user=random.choice(users)),
            anime = random.choice(animes),
            rate = random.randint(0, 10),
        ) for _ in range(round(NUM_PERSON * ACTION_MULTIPLIER))]