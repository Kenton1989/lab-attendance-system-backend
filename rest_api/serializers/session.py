from django.db.models import Q
from django.core.validators import MinValueValidator

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import PrimaryKeyRelatedField, IntegerField, SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from rest_api.models import Session, StudentMakeUpSession, Group, User, Week
from .base import BaseModelSerializer
from .user import UserSerializer
from .group import GroupSerializer
from .week import WeekSerializer


class StartEndTimeValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'start_datetime' in serializer.initial_data or 'end_datetime' in serializer.initial_data:
            get = serializer.make_latest_field_getter(attrs)

            start_datetime = get('start_datetime')
            end_datetime = get('end_datetime')

            if end_datetime < start_datetime:
                raise ValidationError(
                    'start_datetime must be earlier than end_datetime')


class TimeOverlappingWithinGroupValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if ('start_datetime' in serializer.initial_data or
            'end_datetime' in serializer.initial_data or
                'group' in serializer.initial_data):
            get = serializer.make_latest_field_getter(attrs)

            group = get('group_id', 'group')
            start_datetime = get('start_datetime')
            end_datetime = get('end_datetime')

            overlapping = Session.objects.filter(
                start_datetime__lt=end_datetime,
                end_datetime__gt=start_datetime,
                group=group,
            )

            # eliminate the session being updated
            if serializer.instance:
                overlapping.exclude(id=serializer.instance.id)

            if overlapping.exists():
                raise ValidationError(
                    'session is overlapping with another session of the same group')


class SessionSerializer(BaseModelSerializer):
    group = GroupSerializer(read_only=True)
    group_id = PrimaryKeyRelatedField(
        source='group',  queryset=Group.objects.all())

    check_in_deadline_mins = IntegerField(validators=[MinValueValidator(0)])

    week = SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id',
                  'group', 'group_id',
                  'start_datetime', 'end_datetime', 'week',
                  'is_compulsory', 'allow_late_check_in', 'check_in_deadline_mins',
                  'is_active']
        validators = [
            StartEndTimeValidator(),
            TimeOverlappingWithinGroupValidator()
        ]

    def get_week(self, obj: Session):
        start_datetime = obj.start_datetime
        start_date = start_datetime.date()
        q = Week.objects.filter(
            monday__lte=start_date,
            next_monday__gt=start_date
        )
        if q.exists():
            return WeekSerializer(instance=q.first(), fields=['id', 'name']).data
        else:
            return None


class OriginalMakeUpSessionValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'original_session' in serializer.initial_data or 'make_up_session' in serializer.initial_data:
            get = serializer.make_latest_field_getter(attrs)

            original_session = get('original_session')
            make_up_session = get('make_up_session')

            if original_session.id == make_up_session.id:
                raise ValidationError(
                    'original_session and make_up_session cannot be the same session')

            if original_session.group.id == make_up_session.group.id:
                raise ValidationError(
                    'original_session and make_up_session cannot be the sessions of the same group')

            if original_session.group.course.id != make_up_session.group.course.id:
                raise ValidationError(
                    'original_session and make_up_session must be the sessions of the same course')


class UserInOriginalGroupValidator:
    requires_context = True

    def __call__(self, attrs, serializer: BaseModelSerializer):
        if 'original_session' in serializer.initial_data or 'user' in serializer.initial_data:
            get = serializer.make_latest_field_getter(attrs)

            original_session = get('original_session')
            user = get('user')

            if not Session.objects.filter(
                    pk=original_session.id,
                    group__students=user).exists():
                raise ValidationError(
                    'user must be a student of the group of original_session')


class StudentMakeUpSessionSerializer(BaseModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        source='user',  queryset=User.objects.all())

    original_session = SessionSerializer(read_only=True)
    original_session_id = PrimaryKeyRelatedField(
        source='original_session',  queryset=Session.objects.all())

    make_up_session = SessionSerializer(read_only=True)
    make_up_session_id = PrimaryKeyRelatedField(
        source='make_up_session',  queryset=Session.objects.all())

    class Meta:
        model = StudentMakeUpSession
        fields = ['id', 'user',  'user_id',
                  'original_session', 'original_session_id',
                  'make_up_session', 'make_up_session_id']

        validators = [
            UniqueTogetherValidator(
                queryset=StudentMakeUpSession.objects.all(),
                fields=('user', 'original_session')
            ),
            UniqueTogetherValidator(
                queryset=StudentMakeUpSession.objects.all(),
                fields=('user', 'make_up_session')
            ),
            OriginalMakeUpSessionValidator(),
            UserInOriginalGroupValidator(),
        ]
