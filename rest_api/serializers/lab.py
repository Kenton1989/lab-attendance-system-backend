from django.core.validators import MinValueValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_api.models import Lab, User
from .base import BaseModelSerializer
from .user import UserSerializer


class IncreasingLabRoomCountValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):

        if serializer.instance and 'room_count' in attrs:
            room_count = attrs.get('room_count')
            if serializer.instance.room_count > room_count:
                raise ValidationError(
                    'room_count cannot be smaller than existing value')


class LabSerializer(BaseModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='user',
        many=False,
        read_only=True
    )

    room_count = serializers.IntegerField(
        validators=(MinValueValidator(1),)
    )

    username = serializers.CharField(source="user.username",
                                     read_only=True)
    display_name = serializers.CharField(source="user.display_name",
                                         read_only=True)

    executives = UserSerializer(many=True, read_only=True)
    executive_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=User.objects.all(),  # TODO: limit to staff
    )

    class Meta:
        model = Lab
        fields = ['id', 'username', 'display_name',
                  'room_count',
                  'executives', 'executive_ids',
                  'is_active']
        default_exclude_fields = ['executives']
        validators = [
            IncreasingLabRoomCountValidator()
        ]
