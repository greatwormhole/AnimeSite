from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):

    help = 'Creates usergroups'

    @transaction.atomic
    def handle(self, *args, **kwargs) :

        self.stdout.write('Updating groups...')

        moderators = Group.objects.get_or_create(name='Moderators')[0]
        moderate_users = Group.objects.get_or_create(name='Simple users')[0]
        blocked_users = Group.objects.get_or_create(name='Blocked users')[0]
        
        for permission in Permission.objects.all():
            moderators.permissions.remove(permission)
            moderate_users.permissions.remove(permission)
            blocked_users.permissions.remove(permission)

        for permission in Permission.objects.filter(
            Q(content_type__app_label='main')
        ):
            if permission.codename == 'view_' + permission.content_type.model:
                moderate_users.permissions.add(permission)
                moderators.permissions.add(permission)

        for permission in Permission.objects.filter(
            Q(content_type__app_label='main')
        ):
            moderators.permissions.add(permission)