from rest_framework import serializers
from rest_api.models import Week
from datetime import timedelta

ONE_WEEK = timedelta(days=7)
class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['name', 'monday', 'next_monday']
        read_only_fields = ['next_monday']

    
    def create(self, validated_data):
        self.add_next_monday(validated_data)
        return super().create(validated_data)

    def update(self, validated_data):
        self.add_next_monday(validated_data)
        return super().update(validated_data)

    def add_next_monday(self, validated_data):
        monday = validated_data['monday']
        validated_data['next_monday'] = monday + ONE_WEEK
