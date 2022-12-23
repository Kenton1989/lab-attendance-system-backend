from django.db.models import QuerySet, Q, F, Count, Value
from rest_api.models import StudentAttendance, TeacherAttendance, CheckInState
from typing import Callable


def no_grouping(query_set: QuerySet) -> QuerySet:
    return query_set.annotate(no_grouping=Value(True)).values('no_grouping')


def group_by_course(query_set: QuerySet) -> QuerySet:
    return query_set.annotate(course=F('session__group__course')).values('course')


def group_by_group(query_set: QuerySet) -> QuerySet:
    return query_set.annotate(group=F('session__group')).values('group')


def group_by_attender(query_set: QuerySet) -> QuerySet:
    return query_set.annotate(attender=F('user')).values('attender')


def group_by_attending_teacher(query_set: QuerySet) -> QuerySet:
    return query_set.annotate(teacher=F('session__teacher_attendances__user')).values('teacher')


def _cal_attendance_counts_aggregate_params():
    stat_ranges = {
        'overall': Q(),
        'compulsory': Q(session__is_compulsory=True),
        'non_compulsory': Q(session__is_compulsory=False),
    }

    states = {
        'attend': Q(check_in_state=CheckInState.ATTEND),
        'late': Q(check_in_state=CheckInState.LATE),
        'absent': Q(check_in_state=CheckInState.ABSENT),
    }

    result = {}
    for stat_range, range_filter in stat_ranges.items():
        total_count = Count('pk', filter=range_filter)
        name = '{}_total_count'.format(stat_range)
        result[name] = total_count

        for state, state_filter in states.items():
            name = '{}_{}_count'.format(stat_range, state)
            count = Count('pk', filter=range_filter & state_filter)
            result[name] = count

    return result


_attendance_counts_aggregate_params = _cal_attendance_counts_aggregate_params()


def _cal_attendance_counts(
    queryset: QuerySet,
    grouper: Callable[[QuerySet], QuerySet],
    filter: Q = Q(),
) -> QuerySet:
    q = queryset.filter(filter)
    grouped_q = grouper(q)

    results = grouped_q.annotate(
        **_attendance_counts_aggregate_params
    )

    return results


def cal_student_attendance_counts(
    grouper: Callable[[QuerySet], QuerySet],
    filter: Q = Q(),
    queryset: QuerySet = StudentAttendance.objects.all()
) -> QuerySet:
    return _cal_attendance_counts(queryset=queryset, grouper=grouper, filter=filter)


def cal_teacher_attendance_counts(
    grouper: Callable[[QuerySet], QuerySet],
    filter: Q = Q(),
    queryset: QuerySet = TeacherAttendance.objects.all()
) -> QuerySet:
    return _cal_attendance_counts(queryset=queryset, grouper=grouper, filter=filter)


RESULT_FIELD_NAMES = tuple(_attendance_counts_aggregate_params.keys())
