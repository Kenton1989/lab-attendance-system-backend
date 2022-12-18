from rest_api.models import Lab
from rest_framework import serializers
from .dynamic_field_mixin import DynamicFieldsMixin


class LabSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='user',
        many=False,
        read_only=True
    )

    username = serializers.CharField(source="user.username")
    display_name = serializers.CharField(source="user.display_name")

    class Meta:
        model = Lab
        fields = ['id', 'username', 'display_name',
                  'room_count', 'is_active']
