from rest_api.models import User, Lab
from .common import StaffManagedObjectPermission


class LabAccessPermission(StaffManagedObjectPermission):
    def get_managed_data(self, user: User, object_queryset=Lab.objects.all()):
        return object_queryset.filter(executives=user)

    def get_managers(self, obj: Lab, user_queryset=User.objects.all()):
        return user_queryset.filter(executive_of_labs=obj)
