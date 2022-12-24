from rest_api.models import Course, User
from rest_framework.serializers import PrimaryKeyRelatedField
from .base import BaseModelSerializer
from .user import UserSerializer


class CourseSerializer(BaseModelSerializer):
    coordinators = UserSerializer(read_only=True, many=True)
    coordinator_ids = PrimaryKeyRelatedField(
        source='coordinators',
        write_only=True,
        many=True,
        queryset=User.objects.all()  # TODO: limit to staff
    )

    class Meta:
        model = Course
        fields = ['id', 'code', 'title',
                  'coordinators',
                  'coordinator_ids',
                  'is_active']
        default_exclude_fields = ['coordinators']
