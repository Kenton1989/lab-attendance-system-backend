from .base import BaseModelViewSet
from rest_api.serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer
from rest_api.models import StudentAttendance, TeacherAttendance, Course, Group, Session, User
from django_filters import rest_framework as filters
from rest_api.permissions import StudentAttendanceAccessPermission, TeacherAttendanceAccessPermission
from .filters import WeekFilter


class AttendanceFilterSet(filters.FilterSet):
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
    attender = filters.ModelChoiceFilter(
        field_name='attender',
        queryset=Session.objects.all(),
    )
    session_start_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='session__start_datetime')
    session_week = WeekFilter(
        field_name='session__start_datetime')
    check_in_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='check_in_datetime')
    check_in_week = WeekFilter(
        field_name='check_in_datetime')

    is_active = filters.BooleanFilter(field_name='is_active')


class BaseAttendanceViewSet(BaseModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AttendanceFilterSet


class StudentAttendanceViewSet(BaseAttendanceViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer

    permission_classes = (StudentAttendanceAccessPermission,)


class TeacherAttendanceViewSet(BaseAttendanceViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer

    permission_classes = (TeacherAttendanceAccessPermission,)
