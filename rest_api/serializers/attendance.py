from rest_api.models import StudentAttendance, TeacherAttendance, User, Session
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import PrimaryKeyRelatedField, DateTimeField
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from .base import BaseModelSerializer
from .user import UserSerializer
from .session import SessionSerializer


def validate_time_earlier_than_now(datetime_value):
    now = timezone.now()
    if datetime_value > now:
        raise ValidationError(
            'last_modify must be earlier than request process time ({now})'.format(now=now.isoformat()))


class UserInRelationshipOfSessionValidator:
    requires_context = True

    def __init__(self, relationship: str):
        self.relationship = relationship

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'session' in attrs or 'attender' in attrs:
            get = serializer.make_latest_field_getter(attrs)

            session = get('session')
            attender = get('attender')

            if not Session.objects.filter(
                    pk=session.id,
                    **{self.relationship: attender}).exists():
                raise ValidationError(
                    'attender must be a student of the group of session')


class BaseAttendanceSerializer(BaseModelSerializer):
    attender = UserSerializer(read_only=True)
    attender_id = PrimaryKeyRelatedField(
        source='attender',  queryset=User.objects.all())

    session = SessionSerializer(read_only=True)
    session_id = PrimaryKeyRelatedField(
        source='session',  queryset=Session.objects.all())

    last_modify = DateTimeField(
        default=timezone.now,
        validators=(validate_time_earlier_than_now,)
    )

    class Meta:
        fields = ('id',
                  'session', 'session_id',
                  'attender', 'attender_id',
                  'check_in_state', 'check_in_datetime',
                  'last_modify', 'remark', 'is_active')
        validators = []


class StudentAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = StudentAttendance
        validators = [
            UniqueTogetherValidator(
                queryset=StudentAttendance.objects.all(),
                fields=('session', 'attender')
            ),
            UserInRelationshipOfSessionValidator('group__students'),
        ] + BaseAttendanceSerializer.Meta.validators


class TeacherAttendanceSerializer(BaseAttendanceSerializer):
    class Meta(BaseAttendanceSerializer.Meta):
        model = TeacherAttendance
        validators = [
            UniqueTogetherValidator(
                queryset=TeacherAttendance.objects.all(),
                fields=('session', 'attender')
            ),
            UserInRelationshipOfSessionValidator('group__teachers'),
        ] + BaseAttendanceSerializer.Meta.validators
