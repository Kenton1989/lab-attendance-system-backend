from django.db import models
from .user import User


class Lab(models.Model):
    user = models.OneToOneField(
        User,
        related_name='lab_info',
        on_delete=models.CASCADE,
        primary_key=True
    )
    room_count = models.IntegerField(
        null=True,
    )
    is_active = models.BooleanField(default=True)

    executives = models.ManyToManyField(
        User,
        related_name='executive_of_labs'
    )

    def __str__(self):
        return self.user.username
