from rest_framework.serializers import PrimaryKeyRelatedField, IntegerField, CharField
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
            room_no: int = get('room_no', None, True)
            if room_no is not None and room_no > lab.room_count:
                raise ValidationError('room_no exceeds lab room count')


class GroupSerializer(BaseModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = PrimaryKeyRelatedField(
        source='course',  queryset=Course.objects.all())

    lab = LabSerializer(
        read_only=True,
    )
    lab_id = PrimaryKeyRelatedField(
        source='lab',  queryset=Lab.objects.all())

    teachers = UserSerializer(read_only=True, many=True)
    teacher_ids = PrimaryKeyRelatedField(
        source='teachers',
        many=True,
        required=False,
        queryset=User.objects.all()  # TODO: limit to TA
    )

    supervisors = UserSerializer(read_only=True, many=True)
    supervisor_ids = PrimaryKeyRelatedField(
        source='supervisors',
        many=True,
        required=False,
        queryset=User.objects.all()  # TODO: limit to staff
    )

    room_no = IntegerField(
        validators=[MinValueValidator(1)], allow_null=True, required=False)

    class Meta:
        model = Group
        fields = ['id', 'course', 'course_id', 'name',
                  'lab', 'lab_id', 'room_no',
                  'teachers', 'teacher_ids',
                  'supervisors', 'supervisor_ids',
                  'is_active']
        default_exclude_fields = ['supervisors', 'teachers']

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
        if ('group' in attrs or 'student' in attrs):
            get = serializer.make_latest_field_getter(attrs)
            group = get('group')
            student = get('student')
            course = group.course
            conflict = GroupStudent.objects.filter(
                group__course=course,
                student=student
            )

            if serializer.instance is not None:
                conflict = conflict.exclude(pk=serializer.instance.id)

            # print(conflict)

            if conflict.exists():
                raise ValidationError(
                    'the student is already in another group of the same course')


class GroupStudentSerializer(BaseModelSerializer):
    student = UserSerializer(read_only=True)
    student_id = PrimaryKeyRelatedField(
        source='student',  queryset=User.objects.all())

    group = GroupSerializer(read_only=True)
    group_id = PrimaryKeyRelatedField(
        source='group',  queryset=Group.objects.all())

    seat = CharField(default=None)

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
