
from rest_framework import serializers
from rest_api.models import StudentAttendance, TeacherAttendance

COMMON_FIELDS = ['id', 'session', 'user',
                 'check_in_state', 'check_in_datetime',
                 'last_modify', 'remark', 'is_active']


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = COMMON_FIELDS

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = COMMON_FIELDS