from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from rest_api.models import Group, GroupStudent, Course, User
from .user import UserSerializer
from .course import CourseSerializer
from .base import BaseModelSerializer
from .lab import LabSerializer


class GroupSerializer(BaseModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = PrimaryKeyRelatedField(
        source='course', write_only=True, queryset=Course.objects.all())

    lab = LabSerializer(read_only=True)
    lab_id = PrimaryKeyRelatedField(
        source='lab', write_only=True, queryset=Course.objects.all())

    class Meta:
        model = Group
        fields = ['id', 'course', 'course_id', 'name',
                  'lab', 'lab_id', 'room_no',
                  'is_active']

        validators = [
            UniqueTogetherValidator(
                queryset=Group.objects.all(),
                fields=('course', 'name')
            )
        ]


class GroupStudentSerializer(BaseModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = PrimaryKeyRelatedField(
        source='student', write_only=True, queryset=User.objects.all())

    group = GroupSerializer(read_only=True)
    group_id = PrimaryKeyRelatedField(
        source='group', write_only=True, queryset=Group.objects.all())

    class Meta:
        model = GroupStudent
        fields = ['id', 'student', 'student_id', 'group', 'group_id', 'seat']
        validators = [
            UniqueTogetherValidator(
                queryset=GroupStudent.objects.all(),
                fields=('student', 'group')
            )
        ]
