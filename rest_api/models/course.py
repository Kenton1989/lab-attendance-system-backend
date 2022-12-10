from django.db import models
from .user import User

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)

    coordinators = models.ManyToManyField(
        User,
        related_name='coordinator_of_courses'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} [{self.id}]'