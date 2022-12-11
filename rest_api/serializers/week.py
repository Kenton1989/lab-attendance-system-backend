from rest_framework import serializers
from rest_api.models import Week
from datetime import timedelta

ONE_WEEK = timedelta(days=7)
class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['name', 'monday', 'next_monday']

    def validate(self, data):
        if data['next_monday'] - data['monday'] != ONE_WEEK:
            raise serializers.ValidationError('next_monday must be exactly 7 days after monday')

        return super().validate(data)

