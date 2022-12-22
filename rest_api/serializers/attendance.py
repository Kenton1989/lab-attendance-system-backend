from rest_api.models import StudentAttendance, TeacherAttendance, User, Session
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import PrimaryKeyRelatedField, DateTimeField
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from .base import BaseModelSerializer
from .user import UserSerializer
from .session import SessionSerializer


class UserInRelationshipOfSessionValidator:
    requires_context = True

    def __init__(self, relationship: str):
        self.relationship = relationship

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'session' in attrs or 'user' in attrs:
            get = serializer.make_latest_field_getter(attrs)

            session = get('session')
            user = get('user')

            if not Session.objects.filter(
                    pk=session.id,
                    **{self.relationship: user}).exists():
                raise ValidationError(
                    'user must be a student of the group of session')


class BaseAttendanceSerializer(BaseModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        source='user', write_only=True, queryset=User.objects.all())

    session = SessionSerializer(read_only=True)
    session_id = PrimaryKeyRelatedField(
        source='session', write_only=True, queryset=Session.objects.all())

    last_modify = DateTimeField(default=timezone.now)

    class Meta:
        fields = ['id',
                  'session', 'session_id',
                  'user', 'user_id',
                  'check_in_state', 'check_in_datetime',
                  'last_modify', 'remark', 'is_active']
        validators = []


class StudentAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = StudentAttendance
        validators = [
            UniqueTogetherValidator(
                queryset=StudentAttendance.objects.all(),
                fields=('session', 'user')
            ),
            UserInRelationshipOfSessionValidator('group__students'),
        ] + BaseAttendanceSerializer.Meta.validators


class TeacherAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = TeacherAttendance
        validators = [
            UniqueTogetherValidator(
                queryset=TeacherAttendance.objects.all(),
                fields=('session', 'user')
            ),
            UserInRelationshipOfSessionValidator('group__teachers'),
        ] + BaseAttendanceSerializer.Meta.validators
