from django.db import models
from .course import Course
from .user import User

class Group(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    name = models.CharField('group name', max_length=20)
    is_active = models.BooleanField(default=True)

    supervisors = models.ManyToManyField(
        User,
        related_name='supervisor_of_groups'
    )
    teachers = models.ManyToManyField(
        User,
        related_name='teacher_of_groups'
    )
    students = models.ManyToManyField(
        User,
        related_name='student_of_groups',
        through='GroupStudent',
        through_fields=('group', 'student'),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'name'],
                name='unique_course_group',
                violation_error_message='Group name should be unique under a course.'
            )
        ]

    def __str__(self):
        return f'{self.course.code} {self.name} [{self.id}]'


class GroupStudent(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='+'
    )

    seat = models.CharField(max_length=20, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'student'],
                name='unique_group_student',
                violation_error_message='Student should be unique under a group.'
            )
        ]
