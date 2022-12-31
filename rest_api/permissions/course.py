from rest_api.models import User, Course
from .common import StaffManagedObjectPermission


class CourseAccessPermission(StaffManagedObjectPermission):
    def get_managed_data(self, user: User, object_queryset=Course.objects.all()):
        return object_queryset.filter(coordinators=user)

    def get_managers(self, obj: Course, user_queryset=User.objects.all()):
        return user_queryset.filter(coordinator_of_courses=obj)
