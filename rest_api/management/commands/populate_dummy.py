from django.core.management.base import BaseCommand, CommandError
from rest_api.models.dummy_init import create_all_dummy


class Command(BaseCommand):
    help = 'populate the database with dummy data'

    def handle(self, *args, **options):
        create_all_dummy()
