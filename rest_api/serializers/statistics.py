from rest_framework import serializers
from .user import UserSerializer
from .course import CourseSerializer
from .group import GroupSerializer
from .mixins import DynamicFieldsMixin
from rest_api.models import User, Course, Group


class BaseAttendanceCountsSerializer(DynamicFieldsMixin, serializers.Serializer):
    course = serializers.IntegerField(required=False)
    group = serializers.IntegerField(required=False)
    teacher = serializers.IntegerField(required=False)
    attender = serializers.IntegerField(required=False)

    overall_total_count = serializers.IntegerField(read_only=True)
    overall_attend_count = serializers.IntegerField(read_only=True)
    overall_late_count = serializers.IntegerField(read_only=True)
    overall_absent_count = serializers.IntegerField(read_only=True)
    overall_attend_rate = serializers.FloatField(read_only=True)
    overall_late_rate = serializers.FloatField(read_only=True)
    overall_absent_rate = serializers.FloatField(read_only=True)

    compulsory_total_count = serializers.IntegerField(read_only=True)
    compulsory_attend_count = serializers.IntegerField(read_only=True)
    compulsory_late_count = serializers.IntegerField(read_only=True)
    compulsory_absent_count = serializers.IntegerField(read_only=True)
    compulsory_attend_rate = serializers.FloatField(read_only=True)
    compulsory_late_rate = serializers.FloatField(read_only=True)
    compulsory_absent_rate = serializers.FloatField(read_only=True)

    non_compulsory_total_count = serializers.IntegerField(read_only=True)
    non_compulsory_attend_count = serializers.IntegerField(read_only=True)
    non_compulsory_late_count = serializers.IntegerField(read_only=True)
    non_compulsory_absent_count = serializers.IntegerField(read_only=True)
    non_compulsory_attend_rate = serializers.FloatField(read_only=True)
    non_compulsory_late_rate = serializers.FloatField(read_only=True)
    non_compulsory_absent_rate = serializers.FloatField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        results = super().to_representation(instance)
        if 'course' in results:
            results['course'] = self.get_course(results)
        elif 'group' in results:
            results['group'] = self.get_group(results)
        elif 'attender' in results:
            results['attender'] = self.get_attender(results)
        elif 'teacher' in results:
            results['teacher'] = self.get_teacher(results)

        return results

    def get_course(self, obj):
        return CourseSerializer(Course.objects.get(pk=obj['course'])).data

    def get_group(self, obj):
        return GroupSerializer(Group.objects.get(pk=obj['group'])).data

    def get_attender(self, obj):
        return UserSerializer(User.objects.get(pk=obj['attender'])).data

    def get_teacher(self, obj):
        return UserSerializer(User.objects.get(pk=obj['teacher'])).data


class StudentAttendanceCountsSerializer(BaseAttendanceCountsSerializer):
    pass


class TeacherAttendanceCountsSerializer(BaseAttendanceCountsSerializer):
    pass
