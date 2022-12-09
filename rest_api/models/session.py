from django.db import models
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
    room_no = models.IntegerField(blank=True)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    is_compulsory = models.BooleanField(default=True)
    allow_late_check_in = models.BooleanField(default=True)
    check_in_deadline = models.DateTimeField()

    make_up_students = models.ManyToManyField(
        User,
        related_name='make_up_sessions',
        through='MakeUpRelationship',
        through_fields=('original_session', 'student')
    )

    is_active = models.BooleanField()


class MakeUpRelationship(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    original_session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='original_session_of_make_up_relationship'
    )

    make_up_session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='make_up_session_of_make_up_relationship'
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