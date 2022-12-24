from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer
from rest_api.models import StudentAttendance, TeacherAttendance, Course, Group, Session, User
from django_filters import rest_framework as filters


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
    check_in_time = filters.IsoDateTimeFromToRangeFilter()
    session_start_time = filters.IsoDateTimeFromToRangeFilter()


class StudentAttendanceViewSet(ModelViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AttendanceFilterSet


class TeacherAttendanceViewSet(ModelViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AttendanceFilterSet
