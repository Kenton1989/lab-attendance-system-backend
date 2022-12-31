from rest_api.models import User
from .common import StaffManagedObjectPermission


class UserAccessPermission(StaffManagedObjectPermission):
    def get_managed_data(self, user: User, object_queryset=User.objects.all()):
        return object_queryset.filter(pk=user.id)

    def get_managers(self, obj: User, user_queryset=User.objects.all()):
        return user_queryset.filter(pk=obj.id)
