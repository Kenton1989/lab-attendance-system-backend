from rest_api.models import Group, GroupStudent, Course
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .user import UserSerializer
from .course import CourseSerializer
from .dynamic_field_mixin import DynamicFieldsMixin


class GroupSerializer(DynamicFieldsMixin, ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = PrimaryKeyRelatedField(source='course', read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'course', 'course_id', 'name', 'is_active']
        default_exclude_fields = ['course_id']


class GroupStudentSerializer(DynamicFieldsMixin, ModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = PrimaryKeyRelatedField(source='student', read_only=True)

    group = GroupSerializer(read_only=True)
    group_id = PrimaryKeyRelatedField(source='group', read_only=True)

    class Meta:
        model = GroupStudent
        fields = ['id', 'student', 'student_id', 'group', 'group_id', 'seat']
        default_exclude_fields = ['student_id', 'group_id']
