from rest_framework import mixins, viewsets, exceptions, serializers
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_api.models import StudentAttendance, TeacherAttendance, Course, Group, User
from rest_api.statistics import attendance_stat
from rest_api.serializers import StudentAttendanceStatsSerializer, TeacherAttendanceStatsSerializer
from .schemas import StudentAttendanceStatisticsSchema, TeacherAttendanceStatisticsSchema


class BaseAttendanceFilter(filters.FilterSet):
    course = filters.ModelChoiceFilter(
        field_name='session__group__course',
        queryset=Course.objects.all()
    )
    group = filters.ModelChoiceFilter(
        field_name='session__group',
        queryset=Group.objects.all()
    )
    course_coordinators_contain = filters.ModelChoiceFilter(
        field_name='session__group__course__coordinators',
        queryset=User.objects.all()
    )
    group_supervisors_contain = filters.ModelChoiceFilter(
        field_name='session__group__supervisors',
        queryset=User.objects.all()
    )

    class Meta:
        pass


class StudentAttendanceFilter(BaseAttendanceFilter):
    student = filters.ModelChoiceFilter(
        field_name='attender',
        queryset=User.objects.all()
    )
    attending_teachers_contain = filters.ModelChoiceFilter(
        field_name='session__teacher_attendances__attender',
        queryset=User.objects.all()
    )
    group_teachers_contain = filters.ModelChoiceFilter(
        field_name='session__group__teachers',
        queryset=User.objects.all()
    )


class TeacherAttendanceFilter(BaseAttendanceFilter):
    teacher = filters.ModelChoiceFilter(
        field_name='attender',
        queryset=User.objects.all()
    )


class BaseAttendanceStatViewSet(mixins.ListModelMixin,
                                viewsets.GenericViewSet):

    filter_backends = [OrderingFilter]
    ordering_fields = attendance_stat.RESULT_FIELD_NAMES

    pre_grouping_filter_class = filters.FilterSet
    valid_grouping = {}

    def get_grouped_results(self, grouper, queryset):
        return attendance_stat.cal_student_attendance_stat(grouper=grouper, queryset=queryset)

    def get_queryset(self):
        grouping = self.request.query_params.get('grouping', '')
        grouper = self.valid_grouping.get(grouping, None)
        if grouper is None:
            raise exceptions.ValidationError({
                'grouping': ['grouping is unknown'],
            })

        res = self.queryset
        pre_grouping_filter = self.pre_grouping_filter_class(
            data=self.request.query_params, queryset=res)
        if not pre_grouping_filter.is_valid():
            raise exceptions.ValidationError(pre_grouping_filter.errors)
        res = pre_grouping_filter.filter_queryset(res)

        res = self.get_grouped_results(grouper=grouper, queryset=res)
        return res


class StudentAttendanceStatsViewSet(BaseAttendanceStatViewSet):
    schema = StudentAttendanceStatisticsSchema()

    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceStatsSerializer

    pre_grouping_filter_class = StudentAttendanceFilter
    valid_grouping = {
        '': attendance_stat.no_grouping,
        'course': attendance_stat.group_by_course,
        'group': attendance_stat.group_by_group,
        'attender': attendance_stat.group_by_attender,
        'teacher': attendance_stat.group_by_attending_teacher,
    }

    def get_grouped_results(self, grouper, queryset):
        return attendance_stat.cal_student_attendance_stat(grouper=grouper, queryset=queryset)


class TeacherAttendanceStatsViewSet(BaseAttendanceStatViewSet):
    schema = TeacherAttendanceStatisticsSchema()

    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceStatsSerializer

    pre_grouping_filter_class = TeacherAttendanceFilter
    valid_grouping = {
        '': attendance_stat.no_grouping,
        'course': attendance_stat.group_by_course,
        'group': attendance_stat.group_by_group,
        'attender': attendance_stat.group_by_attender,
    }

    def get_grouped_results(self, grouper, queryset):
        return attendance_stat.cal_teacher_attendance_stat(grouper=grouper, queryset=queryset)
