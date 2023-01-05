from django.db.models import QuerySet
from django.utils import timezone
from rest_api.models import User, StudentAttendance, TeacherAttendance, Session, Course
from rest_api.serializers import StudentAttendanceSerializer, TeacherAttendanceSerializer
from .common import StaffManagedObjectPermission
from rest_api.permissions.common import is_superuser, in_group
from datetime import datetime, timedelta
from rest_api.dynamic_preferences_registry import preferences
from .session import SessionAccessPermission


class BaseAttendanceAccessPermission(StaffManagedObjectPermission):
    _session_permission = SessionAccessPermission()

    def has_create_object_permission(self, user, request, view, serializer):
        assert isinstance(serializer,
                          (StudentAttendanceSerializer, TeacherAttendanceSerializer))
        session: Session = serializer['session']
        return (
            self._can_check_in(user, session, timezone.now()) or
            self._session_permission.has_update_object_permission(
                user, request, view, session)
        )

    def has_update_object_permission(self, user, request, view, obj):
        assert isinstance(obj, (StudentAttendance, TeacherAttendance))
        session = obj.session
        return (
            self._can_check_in(user, session, timezone.now()) or
            super().has_update_object_permission(user, request, view, obj)
        )

    def get_managed_data(self, user: User, object_queryset: QuerySet) -> QuerySet:
        sessions = self._session_permission.get_managed_data(user)
        return object_queryset.filter(session__in=sessions)

    def get_managers(self,
                     obj: StudentAttendance | TeacherAttendance,
                     user_queryset: QuerySet = User.objects.all()) -> QuerySet:
        session = obj.session
        return self._session_permission.get_managers(session, user_queryset)

    def get_course_options(self, user: User, course_queryset=Course.objects.all()) -> QuerySet:
        if is_superuser(user):
            return course_queryset

        if in_group(user, 'staff'):
            return course_queryset

        return course_queryset.none()

    def _can_check_in(self, user: User, session: Session, request_time: datetime):
        return (
            session.group.lab.user == user and
            self._is_in_check_in_period(session, request_time)
        )

    def _is_in_check_in_period(self, session: Session, request_time: datetime):
        return (
            request_time >= self._get_check_in_start_time(session) and
            request_time <= self._get_check_in_end_time(session)
        )

    def _get_check_in_start_time(self, session: Session) -> datetime:
        return session.start_datetime - timedelta(minutes=preferences['session__earliest_check_in_minutes'])

    def _get_check_in_end_time(self, session: Session) -> datetime:
        session = session
        if session.is_compulsory and not session.allow_late_check_in:
            return session.start_datetime + timedelta(minutes=session.check_in_deadline_mins)
        else:
            return session.end_datetime


class StudentAttendanceAccessPermission(BaseAttendanceAccessPermission):
    def get_managed_data(self, user: User, object_queryset: QuerySet = StudentAttendance.objects.all()) -> QuerySet:
        return super().get_managed_data(user, object_queryset)

    def get_course_options(self, user: User, course_queryset=Course.objects.all()) -> QuerySet:
        if in_group(user, 'student'):
            return course_queryset.filter(groups__sessions__student_attendances__attender=user).distinct()
        return super().get_course_options(user, course_queryset)


class TeacherAttendanceAccessPermission(BaseAttendanceAccessPermission):
    def get_managed_data(self, user: User, object_queryset: QuerySet = TeacherAttendance.objects.all()) -> QuerySet:
        return super().get_managed_data(user, object_queryset)

    def get_course_options(self, user: User, course_queryset=Course.objects.all()) -> QuerySet:
        if in_group(user, 'teacher'):
            return course_queryset.filter(groups__sessions__teacher_attendances__attender=user).distinct()
        return super().get_course_options(user, course_queryset)
