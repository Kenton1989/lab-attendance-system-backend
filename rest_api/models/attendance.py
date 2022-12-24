from django.db import models
from .session import Session
from .user import User
from django.utils import timezone


class CheckInState:
    ABSENT = 'absent'
    LATE = 'late'
    ATTEND = 'attend'


CHECK_IN_STATE_CHOICES = [
    (CheckInState.ABSENT, 'absent'),
    (CheckInState.LATE, 'late'),
    (CheckInState.ATTEND, 'attend'),
]


class AbstractAttendance(models.Model):
    check_in_state = models.CharField(
        choices=CHECK_IN_STATE_CHOICES,
        max_length=20,
        default=CheckInState.ABSENT
    )

    check_in_datetime = models.DateTimeField(null=True)

    last_modify = models.DateTimeField(default=timezone.now)

    remark = models.CharField(max_length=200, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class StudentAttendance(AbstractAttendance):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='student_attendances'
    )

    attender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_attendances'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'attender'],
                name='unique_student_attendance_session',
                violation_error_message='only one attendance record allowed per session per student'
            )
        ]

        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['attender', 'session']),
        ]


class TeacherAttendance(AbstractAttendance):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='teacher_attendances'
    )

    attender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_attendances'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'attender'],
                name='unique_teacher_attendance_session',
                violation_error_message='only one attendance record allowed per session per teacher'
            )
        ]

        indexes = [
            models.Index(fields=['session']),
            models.Index(fields=['attender', 'session']),
        ]
