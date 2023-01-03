from .base import UserManagedObjectViewSet
from rest_api import models, permissions
from .course import CourseViewSet
from .group import GroupViewSet
from .lab import LabViewSet


class UserManagedCourseViewSet(UserManagedObjectViewSet):
    serializer_class = CourseViewSet.serializer_class

    filter_backends = CourseViewSet.filter_backends
    search_fields = CourseViewSet.search_fields
    filterset_class = CourseViewSet.filterset_class

    queryset = models.Course.objects.all()
    management_permission_class = permissions.CourseAccessPermission


class UserManagedGroupViewSet(UserManagedObjectViewSet):
    serializer_class = GroupViewSet.serializer_class

    filter_backends = GroupViewSet.filter_backends
    search_fields = GroupViewSet.search_fields
    filterset_class = GroupViewSet.filterset_class

    queryset = models.Group.objects.all()
    management_permission_class = permissions.GroupAccessPermission


class UserManagedLabViewSet(UserManagedObjectViewSet):
    serializer_class = LabViewSet.serializer_class

    filter_backends = LabViewSet.filter_backends
    search_fields = LabViewSet.search_fields
    filterset_class = LabViewSet.filterset_class

    queryset = models.Lab.objects.all()
    management_permission_class = permissions.LabAccessPermission
