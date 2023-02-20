from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.hashers import make_password


class RestApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_api'

    def ready(self):
        post_migrate.connect(receiver=populate_groups, sender=self)


def populate_groups(**kwargs):
    from django.contrib.auth.models import Group
    from rest_api.models import User
    from django.conf import settings

    admin_grp, _ = Group.objects.get_or_create(name='admin')
    Group.objects.get_or_create(name='staff')
    Group.objects.get_or_create(name='lab')
    Group.objects.get_or_create(name='teacher')
    Group.objects.get_or_create(name='student')

    if settings.DEBUG and not User.objects.filter(username='ADMIN').exists():
        admin = User.objects.create_superuser(
            username='ADMIN',
            email='admin@example.com',
            password='12345678',
        )
        admin.groups.add(admin_grp)
        admin.save()
