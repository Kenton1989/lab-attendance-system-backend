from django.db import models
from django.db.models import F, Q
from datetime import timedelta

_MONDAY_CODE = 2


class Week(models.Model):
    name = models.CharField(max_length=20, unique=True)
    monday = models.DateField()
    next_monday = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['monday', 'next_monday']),
        ]
