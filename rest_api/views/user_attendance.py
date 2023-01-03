from django_filters import rest_framework as filters
from rest_api.models import StudentAttendance, TeacherAttendance, Course, Group, Session
from rest_api.permissions import UserRelationshipAccessPermission
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .base import UserRelatedObjectGenericViewSet
from .attendance import StudentAttendanceViewSet, TeacherAttendanceViewSet
from rest_framework.decorators import action


class UserAttendanceFilterSet(filters.FilterSet):
    course = filters.ModelChoiceFilter(
        field_name='session__group__course',
        queryset=Course.objects.all(),
    )
    group = filters.ModelChoiceFilter(
        field_name='session__group',
        queryset=Group.objects.all(),
    )
    session = filters.ModelChoiceFilter(
        field_name='session',
        queryset=Session.objects.all(),
    )
    check_in_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='check_in_datetime')
    session_start_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='session__start_datetime')


class BaseUserAttendanceViewSet(mixins.ListModelMixin, UserRelatedObjectGenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserAttendanceFilterSet

    permission_classes = (UserRelationshipAccessPermission,)

    def get_queryset(self):
        return super().get_queryset().filter(attender=self.queried_user)


class UserStudentAttendanceViewSet(BaseUserAttendanceViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceViewSet.serializer_class

    @action(methods=['get'], detail=False)
    def course_options(self):
        return Course.objects.filter(groups__sessions__student_attendances__attender=self.queried_user).distinct()


class UserTeacherAttendanceViewSet(BaseUserAttendanceViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceViewSet.serializer_class

    @action(methods=['get'], detail=False)
    def course_options(self):
        return Course.objects.filter(groups__sessions__teacher_attendances__attender=self.queried_user).distinct()
