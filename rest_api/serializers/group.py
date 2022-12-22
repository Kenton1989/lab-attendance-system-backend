from rest_framework.serializers import PrimaryKeyRelatedField, IntegerField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import Q

from rest_api.models import Group, GroupStudent, Course, User, Lab
from .user import UserSerializer
from .course import CourseSerializer
from .base import BaseModelSerializer
from .lab import LabSerializer


class MaxLabRoomNoValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'lab' in attrs or 'room_no' in attrs:
            get = serializer.make_latest_field_getter(attrs)
            lab: Lab = get('lab')
            room_no: int = get('room_no')
            if room_no > lab.room_count:
                raise ValidationError('room_no exceeds lab room count')


class GroupSerializer(BaseModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = PrimaryKeyRelatedField(
        source='course', write_only=True, queryset=Course.objects.all())

    lab = LabSerializer(read_only=True)
    lab_id = PrimaryKeyRelatedField(
        source='lab', write_only=True, queryset=Lab.objects.all())

    room_no = IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        model = Group
        fields = ['id', 'course', 'course_id', 'name',
                  'lab', 'lab_id', 'room_no',
                  'is_active']

        validators = [
            UniqueTogetherValidator(
                queryset=Group.objects.all(),
                fields=('course', 'name')
            ),
            MaxLabRoomNoValidator(),
        ]


class UniqueCourseStudentValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'group' in attrs or 'student' in attrs:
            get = serializer.make_latest_field_getter(attrs)
            group = get('group')
            student = get('student')
            course = group.course
            if GroupStudent.objects.filter(
                ~Q(group=group),
                group__course=course,
                student=student
            ).exists():
                raise ValidationError(
                    'the student is already in another group of the same course')


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
                fields=('group', 'student')
            ),
            UniqueTogetherValidator(
                queryset=GroupStudent.objects.all(),
                fields=('group', 'seat')
            ),
            UniqueCourseStudentValidator(),
        ]
