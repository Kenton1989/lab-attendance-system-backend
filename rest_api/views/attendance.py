from .base import BaseModelViewSet
from rest_api.serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer
from rest_api.models import StudentAttendance, TeacherAttendance, Course, Group, Session, User
from django_filters import rest_framework as filters
from rest_api.permissions import StudentAttendanceAccessPermission, TeacherAttendanceAccessPermission
from .filters import WeekFilter
from datetime import datetime
from django.utils import timezone


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
        queryset=User.objects.all(),
    )
    session_start_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='session__start_datetime')
    session_week = WeekFilter(
        field_name='session__start_datetime')
    check_in_state = filters.CharFilter(field_name='check_in_state')
    check_in_time = filters.IsoDateTimeFromToRangeFilter(
        field_name='check_in_datetime')
    check_in_week = WeekFilter(
        field_name='check_in_datetime')

    last_modify = filters.IsoDateTimeFromToRangeFilter(
        field_name='last_modify')

    is_active = filters.BooleanFilter(field_name='is_active')


class BaseAttendanceViewSet(BaseModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AttendanceFilterSet

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get("data", None)

        if data is not None:
            last_modify_in = data.get("last_modify")
            new_last_modify_in = self._cap_last_modify_to_now(last_modify_in)

            if new_last_modify_in is not None:
                data["last_modify"] = new_last_modify_in

        return super().get_serializer(*args, **kwargs)

    def _cap_last_modify_to_now(self, last_modify_in):
        if last_modify_in is None:
            return None

        input_is_datetime = isinstance(last_modify_in, datetime)

        if (input_is_datetime):
            last_modify = last_modify_in
        else:
            try:
                last_modify = datetime.fromisoformat(last_modify_in)
                if last_modify.tzinfo is None:
                    last_modify.tzinfo = timezone.get_current_timezone()
            except:
                return None

        now = timezone.now()
        print(now, last_modify)
        res = min(now, last_modify)

        if input_is_datetime:
            return res
        else:
            return res.isoformat()


class StudentAttendanceViewSet(BaseAttendanceViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer

    permission_classes = (StudentAttendanceAccessPermission,)


class TeacherAttendanceViewSet(BaseAttendanceViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer

    permission_classes = (TeacherAttendanceAccessPermission,)
