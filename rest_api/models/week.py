from django.db import models
from django.db.models import F, Q
from datetime import timedelta
from rest_api.validators import monday_validator


class Week(models.Model):
    name = models.CharField(max_length=20, unique=True)
    monday = models.DateField(validators=[monday_validator])
    next_monday = models.DateField(validators=[monday_validator])

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(next_monday=F('monday')+timedelta(days=7)),
                name='ensure_7_days_gap',
                violation_error_message='next_monday must be exactly 7 days greater then monday',
            )
        ]
