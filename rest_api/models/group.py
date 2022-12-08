from django.db import models
from .course import Course


class Group(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    name = models.CharField('group name')
    is_active = models.BooleanField()

    class Meta:
        constrains = [
            models.UniqueConstraint(
                fields=['course', 'name'],
                name='unique_course_group',
                violation_error_message='Group name should be unique under a course.'
            )
        ]
