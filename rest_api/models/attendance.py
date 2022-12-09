from django.db import models
from .session import Session
from .user import User
from django.utils import timezone


class AbstractAttendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    check_in_state = models.CharField(max_length=20, blank=True)
    check_in_datetime = models.DateTimeField(blank=True)

    last_modify = models.DateTimeField(default=timezone.now)

    remark = models.CharField(max_length=200, blank=True)

    is_active = models.BooleanField()

    class Meta:
        abstract = True

class StudentAttendance(AbstractAttendance):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user'],
                name='unique_student_attendance_session',
                violation_error_message='Only one attendance record allowed per session per student.'
            )
        ]

class TeacherAttendance(AbstractAttendance):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user'],
                name='unique_teacher_attendance_session',
                violation_error_message='Only one attendance record allowed per session per teacher.'
            )
        ]