from rest_framework.exceptions import ValidationError
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from rest_api.models import Session, StudentMakeUpSession, Group, User
from .base import BaseModelSerializer
from .user import UserSerializer
from .group import GroupSerializer


class SessionSerializer(BaseModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = PrimaryKeyRelatedField(
        source='group', write_only=True, queryset=Group.objects.all())

    class Meta:
        model = Session
        fields = ['id',
                  'group', 'group_id',
                  'start_datetime', 'end_datetime',
                  'is_compulsory', 'allow_late_check_in', 'check_in_deadline_mins',
                  'is_active']

    def validate(self, attrs):
        get = self._make_latest_field_getter(attrs)

        start_datetime = get('start_datetime')
        end_datetime = get('end_datetime')

        if end_datetime < start_datetime:
            raise ValidationError(
                'start_datetime must be earlier than end_datetime')
        return super().validate(attrs)


class StudentMakeUpSessionSerializer(BaseModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        source='user', write_only=True, queryset=User.objects.all())

    original_session = SessionSerializer(read_only=True)
    original_session_id = PrimaryKeyRelatedField(
        source='original_session', write_only=True, queryset=Session.objects.all())

    make_up_session = SessionSerializer(read_only=True)
    make_up_session_id = PrimaryKeyRelatedField(
        source='make_up_session', write_only=True, queryset=Session.objects.all())

    class Meta:
        model = StudentMakeUpSession
        fields = ['id', 'user',  'user_id',
                  'original_session', 'original_session_id',
                  'make_up_session', 'make_up_session_id']
        default_exclude_fields = ['user_id',
                                  'original_session_id',
                                  'make_up_session_id']
        validators = [
            UniqueTogetherValidator(
                queryset=StudentMakeUpSession.objects.all(),
                fields=('user', 'original_session')
            ),
            UniqueTogetherValidator(
                queryset=StudentMakeUpSession.objects.all(),
                fields=('user', 'make_up_session')
            )
        ]
