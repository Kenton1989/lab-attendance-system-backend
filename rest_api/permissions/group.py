from django.db.models import Q
from rest_api.models import User, Group, GroupStudent
from rest_api.serializers import GroupSerializer, GroupStudentSerializer
from .common import StaffManagedObjectPermission
from .course import CourseAccessPermission
from .lab import LabAccessPermission


class GroupAccessPermission(StaffManagedObjectPermission):
    _course_permission = CourseAccessPermission()
    _lab_permission = LabAccessPermission()

    def has_create_object_permission(self, user, request, view, serializer):
        assert isinstance(serializer, GroupSerializer)

        course = serializer.data['course']

        return self._course_permission.has_update_object_permission(
            user, request, view, course)

    def get_managed_data(self, user: User, object_queryset=Group.objects.all()):
        course = self._course_permission.get_managed_data(user)
        lab = self._lab_permission.get_managed_data(user)
        query = Q(supervisors=user) | Q(course__in=course) | Q(lab__in=lab)
        return object_queryset.filter(query)

    def get_managers(self, obj: Group, user_queryset=User.objects.all()):
        course_managers = self._course_permission.get_managers(
            obj.course, user_queryset)
        lab_managers = self._lab_permission.get_managers(
            obj.lab, user_queryset)
        return (
            user_queryset.filter(supervisor_of_groups=obj) |
            course_managers |
            lab_managers
        ).distinct()


class GroupStudentAccessPermission(StaffManagedObjectPermission):
    _group_permission = GroupAccessPermission()

    def has_create_object_permission(self, user, request, view, serializer):
        assert isinstance(serializer, GroupStudentSerializer)

        group = serializer.data['group']

        return self._group_permission.has_update_object_permission(
            user, request, view, group)

    def has_destroy_object_permission(self, user, request, view, obj: GroupStudent):
        group = obj.group

        return (
            super().has_destroy_object_permission(user, request, view, obj) or
            self._group_permission.has_update_object_permission(
                user, request, view, group))

    def get_managed_data(self, user: User, object_queryset=GroupStudent.objects.all()):
        groups = self._group_permission.get_managers(user)
        return object_queryset.filter(group_in=groups)

    def get_managers(self, obj: GroupStudent, user_queryset=User.objects.all()):
        return self._group_permission.get_managers(obj.group, user_queryset)
