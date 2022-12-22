from rest_api.models import StudentAttendance, TeacherAttendance, User, Session
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import PrimaryKeyRelatedField, ModelSerializer, DateTimeField
from .base import BaseModelSerializer
from .user import UserSerializer
from .session import SessionSerializer


class BaseAttendanceSerializer(BaseModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        source='user', write_only=True, queryset=User.objects.all())

    session = SessionSerializer(read_only=True)
    session_id = PrimaryKeyRelatedField(
        source='session', write_only=True, queryset=Session.objects.all())

    class Meta:
        fields = ['id',
                  'session', 'session_id',
                  'user', 'user_id',
                  'check_in_state', 'check_in_datetime',
                  'last_modify', 'remark', 'is_active']


class StudentAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = StudentAttendance
        validators = [
            UniqueTogetherValidator(
                queryset=StudentAttendance.objects.all(),
                fields=('session', 'user')
            )
        ]


class TeacherAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = TeacherAttendance
        validators = [
            UniqueTogetherValidator(
                queryset=TeacherAttendance.objects.all(),
                fields=('session', 'user')
            )
        ]
