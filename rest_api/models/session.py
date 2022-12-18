from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator

from .user import User
from .group import Group
from .lab import Lab


def get_default_ddl():
    return 30


class Session(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    room_no = models.IntegerField(
        null=True,
        validators=(MinValueValidator(1),)
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    is_compulsory = models.BooleanField(default=True)
    allow_late_check_in = models.BooleanField(default=True)
    check_in_deadline_mins = models.IntegerField(
        validators=[MinValueValidator(0)], default=get_default_ddl)

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(end_datetime__gte=F('start_datetime')),
                name='session_end_datetime_after_start_datetime',
                violation_error_message='end_datetime must be greater than start_datetime',
            ),
            models.CheckConstraint(check=Q(room_no__gte=1),
                                   name='group_valid_room_number',
                                   violation_error_message='room_no must be positive'),
        ]

        indexes = [
            models.Index(fields=['group', 'lab', 'start_datetime']),
            models.Index(fields=['lab', 'start_datetime']),
            models.Index(fields=['start_datetime']),
        ]


class StudentMakeUpSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_of_student_make_up'
    )

    original_session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='original_of_student_make_up'
    )

    make_up_session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='make_up_of_student_make_up'
    )

    seat = models.CharField(max_length=20, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'original_session'],
                name='unique_original_session_student',
                violation_error_message='Student can make up a session using only one another session.'
            ),
            models.UniqueConstraint(
                fields=['user', 'make_up_session'],
                name='unique_make_up_session_student',
                violation_error_message='Student can only participate one session for at most once.'
            )
        ]

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['original_session']),
            models.Index(fields=['make_up_session']),
        ]
