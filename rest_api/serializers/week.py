from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_api.models import Week
from datetime import date, timedelta
from .base import BaseModelSerializer

_MONDAY_CODE = 0


def monday_validator(value: date) -> None:
    if value.weekday() != _MONDAY_CODE:
        raise ValidationError(
            'the date is not monday')


_ONE_WEEK = timedelta(days=7)


def validate_non_overlapping_monday(monday: date):
    next_monday = monday + _ONE_WEEK

    # if the new week interval overlap with an existing week
    if Week.objects.filter(monday__lt=next_monday, next_monday__gt=monday).exists():
        raise ValidationError('new week is overlapping with an existing week')


class WeekSerializer(BaseModelSerializer):
    monday = serializers.DateField(
        validators=[monday_validator, validate_non_overlapping_monday]
    )

    class Meta:
        model = Week
        fields = ['id', 'name', 'monday', 'next_monday']
        read_only_fields = ['next_monday']

    def create(self, validated_data):
        self._add_next_monday(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._add_next_monday(validated_data)
        return super().update(instance, validated_data)

    def _add_next_monday(self, validated_data):
        monday: date = validated_data.get('monday', None)
        if monday is not None:
            validated_data['next_monday'] = monday + _ONE_WEEK
