from rest_api.models import Lab
from rest_framework import serializers


class LabSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='user',
        many=False,
        read_only=True
    )

    short_name = serializers.CharField(source="user.username")
    full_name = serializers.CharField(source="user.display_name")

    class Meta:
        model = Lab
        fields = ['id', 'short_name', 'full_name',
                  'room_count', 'is_active']
