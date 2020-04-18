from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--username', required=False)
        parser.add_argument('--password', required=False)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        if User.objects.count() == 0:
            print(username, password)
            admin = User.objects.create_superuser(username=username,
                                                  email='',
                                                  password=password)
            admin.is_active = True
            admin.is_superuser = True
            admin.save()
        else:
            print(
                'Admin accounts can only be initialized if no Accounts exist')
