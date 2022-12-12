from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator

from .user import User
from .group import Group
from .lab import Lab


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
    check_in_deadline_mins = models.IntegerField(validators=[MinValueValidator(0)])

    make_up_students = models.ManyToManyField(
        User,
        related_name='make_up_sessions',
        through='MakeUpRelationship',
        through_fields=('original_session', 'student')
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(end_datetime_gte=Q('start_datetime')),
                name='session_end_datetime_after_start_datetime',
                violation_error_message='end_datetime must be greater than start_datetime',
            ),
            models.CheckConstraint(check=Q(lab_room__gte=1),
                                   name='group_valid_room_number',
                                   violation_error_message='room_no must be positive'),
        ]


class MakeUpRelationship(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'
    )

    original_session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='+'
    )

    make_up_session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='+'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'original_session'],
                name='unique_original_session_student',
                violation_error_message='Student can make up a session using only one another session.'
            ),
            models.UniqueConstraint(
                fields=['student', 'make_up_session'],
                name='unique_make_up_session_student',
                violation_error_message='Student can only participate one session for at most once.'
            )
        ]
