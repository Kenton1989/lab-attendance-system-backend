from rest_api.models import Lab
from rest_framework import serializers
from .base import BaseModelSerializer
from django.core.validators import MinValueValidator


class LabSerializer(BaseModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='user',
        many=False,
        read_only=True
    )

    room_count = serializers.IntegerField(
        validators=(MinValueValidator(1),)
    )

    username = serializers.CharField(source="user.username", read_only=True)
    display_name = serializers.CharField(
        source="user.display_name", read_only=True)

    class Meta:
        model = Lab
        fields = ['id', 'username', 'display_name',
                  'room_count', 'is_active']
