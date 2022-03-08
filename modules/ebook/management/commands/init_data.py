from ast import arg
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group as DjangoGroup, Permission
from modules.ebook.models import User
from utils.choices import Role


class Command(BaseCommand):
    help = "Seed initial data into the Database"

    def add_arguments(self, parser):
        parser.add_argument("email", nargs="+", type=str)
        parser.add_argument("password", nargs="+", type=str)
        parser.add_argument("name", nargs="+", type=str)

    def create_groups(self, groups):
        for group in groups:
            _ = DjangoGroup.objects.get_or_create(name=group)
            print(f'\tGroup created "{group}"')

    def create_superuser(self, email, password, name):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            User.objects.create_ebook_superuser(
                email=email, password=password, name=name
            )
            print(f'SUPERUSER Created. email: "{email}". Password: "{password}"')
        else:
            print(f'SUPERUSER "{email}" Exists, Not Creating')

    def handle(self, *args, **options):
        self.create_groups(Role.get_choice_list())

        if not options["email"] or not options["password"] or not options["name"]:
            raise ValueError("Please add all arguments")

        self.create_superuser(
            options["email"][0], options["password"][0], options["name"][0]
        )
