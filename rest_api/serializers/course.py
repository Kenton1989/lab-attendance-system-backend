from rest_api.models import Course
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .dynamic_field_mixin import DynamicFieldsMixin


class CourseSerializer(DynamicFieldsMixin, ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'is_active']
