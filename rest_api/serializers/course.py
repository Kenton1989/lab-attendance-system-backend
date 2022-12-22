from rest_api.models import Course
from .base import BaseModelSerializer


class CourseSerializer(BaseModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'is_active']
