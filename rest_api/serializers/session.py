from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_api.models import Session, StudentMakeUpSession, Lab
from .dynamic_field_mixin import DynamicFieldsMixin
from .user import UserSerializer
from .group import GroupSerializer
from .lab import LabSerializer


class SessionSerializer(DynamicFieldsMixin, ModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = PrimaryKeyRelatedField(source='group', read_only=True)

    lab = LabSerializer(read_only=True)
    lab_id = PrimaryKeyRelatedField(source='lab', queryset=Lab.objects.all())

    class Meta:
        model = Session
        fields = ['id',
                  'group', 'group_id',
                  'lab', 'lab_id', 'room_no',
                  'start_datetime', 'end_datetime',
                  'is_compulsory', 'allow_late_check_in', 'check_in_deadline_mins',
                  'is_active']
        default_exclude_fields = ['lab_id', 'group_id']


class StudentMakeUpSessionSerializer(DynamicFieldsMixin, ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', read_only=True)

    original_session = SessionSerializer(read_only=True)
    original_session_id = PrimaryKeyRelatedField(
        source='original_session', read_only=True)

    make_up_session = SessionSerializer(read_only=True)
    make_up_session_id = PrimaryKeyRelatedField(
        source='make_up_session', queryset=Session.objects.all())

    class Meta:
        model = StudentMakeUpSession
        fields = ['id', 'user',  'user_id',
                  'original_session', 'original_session_id',
                  'make_up_session', 'make_up_session_id']
        default_exclude_fields = ['user_id',
                                  'original_session_id',
                                  'make_up_session_id']
