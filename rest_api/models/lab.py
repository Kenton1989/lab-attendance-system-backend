from django.db import models
from .user import User

class Lab(models.Model):
    user = models.OneToOneField(User, related_name='lab_info')
    room_count = models.IntegerField(blank=True)