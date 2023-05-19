from django.contrib.auth.management.commands import createsuperuser

class Command(createsuperuser.Command):
    help = 'create admin for lab attendance system (LAS)'

    def handle(self, *args, **options):
        from rest_api.models import User
        from django.contrib.auth.models import Group as AuthGroup

        admin_grp = AuthGroup.objects.get(name="admin")

        super().handle(self, *args, **options)

        non_admin_su = User.objects.filter(is_superuser=True).exclude(groups=admin_grp)

        for user in non_admin_su:
            user.username = user.username.upper()
            user.groups.add(admin_grp)
            user.save()
        print(f"added {len(non_admin_su)} user into admin group")



