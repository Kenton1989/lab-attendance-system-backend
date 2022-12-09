from django.db import models
from .user import User

class Lab(models.Model):
    user = models.OneToOneField(
        User,
        related_name='lab_info',
        on_delete=models.CASCADE
    )
    room_count = models.IntegerField(blank=True)

    executives = models.ManyToManyField(
        User,
        related_name='executive_of_labs'
    )

    def __str__(self):
        return self.user.username