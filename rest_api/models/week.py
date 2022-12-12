from django.db import models
from django.db.models import F, Q
from datetime import timedelta, date
from django.core.exceptions import ValidationError

_monday_code = 0


def monday_validator(value: date) -> None:
    if value.weekday() != _monday_code:
        raise ValidationError(
            'The date is not monday.')


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

        indexes = [
            models.Index(fields=['monday', 'next_monday']),
        ]
