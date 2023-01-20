from django_filters import rest_framework as filters
from rest_api.models import StudentAttendance, TeacherAttendance, Course, Group, Session
from rest_api.permissions import UserRelationshipReadOnlyAccessPermission
from rest_framework import mixins
from .base import UserRelatedObjectGenericViewSet
from .attendance import StudentAttendanceViewSet, TeacherAttendanceViewSet, BaseAttendanceViewSet
from .course import CourseViewSet
from rest_framework.decorators import action
from .schemas import UserStudentAttendanceSchema, UserTeacherAttendanceSchema, UserTeacherAttendanceCourseOptionSchema, UserStudentAttendanceCourseOptionSchema


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


class BaseUserAttendanceViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                UserRelatedObjectGenericViewSet):
    filter_backends = BaseAttendanceViewSet.filter_backends
    filterset_class = BaseAttendanceViewSet.filterset_class

    permission_classes = (UserRelationshipReadOnlyAccessPermission,)

    def get_queryset(self):
        return super().get_queryset().filter(attender=self.queried_user)

    # view set for /xxx-attendances/course_options/
    class CourseOptionsViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               UserRelatedObjectGenericViewSet):
        queryset = CourseViewSet.queryset
        serializer_class = CourseViewSet.serializer_class

        filter_backends = CourseViewSet.filter_backends
        search_fields = CourseViewSet.search_fields
        filterset_class = CourseViewSet.filterset_class

        permission_classes = (UserRelationshipReadOnlyAccessPermission,)


class UserStudentAttendanceViewSet(BaseUserAttendanceViewSet):
    schema = UserStudentAttendanceSchema()

    queryset = StudentAttendanceViewSet.queryset
    serializer_class = StudentAttendanceViewSet.serializer_class

    class CourseOptionsViewSet(BaseUserAttendanceViewSet.CourseOptionsViewSet):
        schema = UserStudentAttendanceCourseOptionSchema()

        def get_queryset(self):
            return super().get_queryset().filter(
                groups__sessions__student_attendances__attender=self.queried_user).distinct()


class UserTeacherAttendanceViewSet(BaseUserAttendanceViewSet):
    schema = UserTeacherAttendanceSchema()

    queryset = TeacherAttendanceViewSet.queryset
    serializer_class = TeacherAttendanceViewSet.serializer_class

    class CourseOptionsViewSet(BaseUserAttendanceViewSet.CourseOptionsViewSet):
        schema = UserTeacherAttendanceCourseOptionSchema()

        def get_queryset(self):
            return super().get_queryset().filter(
                groups__sessions__teacher_attendances__attender=self.queried_user).distinct()
