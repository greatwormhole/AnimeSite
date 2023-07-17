from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import AuthUser

class Command(BaseCommand):

    help = 'Deletes fake data'

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Deleting old data...")

        models = apps.get_models()

        for m in models:
            if not issubclass(m, AuthUser):
                m.objects.all().delete()
            else:
                m.objects.all().exclude(is_staff=True).delete()
        
