from rest_api.models import StudentAttendance, TeacherAttendance
from rest_framework.serializers import PrimaryKeyRelatedField, ModelSerializer
from .dynamic_field_mixin import DynamicFieldsMixin
from .user import UserSerializer
from .session import SessionSerializer


class BaseAttendanceSerializer(DynamicFieldsMixin, ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user')

    session = UserSerializer(read_only=True)
    session_id = PrimaryKeyRelatedField(source='session')

    class Meta:
        fields = ['id',
                  'session', 'session_id',
                  'user', 'user_id',
                  'check_in_state', 'check_in_datetime',
                  'last_modify', 'remark', 'is_active']
        default_exclude_fields = ['session', 'user']


class StudentAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = StudentAttendance


class TeacherAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = TeacherAttendance
