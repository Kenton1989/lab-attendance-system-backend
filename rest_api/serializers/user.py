from rest_framework import serializers
from rest_api.models import User
from django.contrib.auth.password_validation import validate_password
from .base import BaseModelSerializer
from .auth_group import AuthGroupSerializer
from django.contrib.auth.models import Group as AuthGroup

from django.core.exceptions import ValidationError
import re

_username_pattern = re.compile(r'^\w+$')


def validate_username(value: str) -> None:
    if not _username_pattern.match(value):
        raise ValidationError(
            'the username can only contain alphabets and digits')


class StoreUppercaseCharField(serializers.CharField):
    def to_internal_value(self, data):
        return super().to_internal_value(data).upper()


class UserSerializer(BaseModelSerializer):
    username = StoreUppercaseCharField(validators=[validate_username])

    password = serializers.CharField(
        write_only=True, validators=[validate_password])

    email = serializers.EmailField()

    roles = AuthGroupSerializer(source='groups', many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        source='groups',
        many=True,
        required=False,
        queryset=AuthGroup.objects.all()  # TODO: limit to staff
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'display_name', 'roles', 'role_ids',
                  'is_active']
        default_exclude_fields = ['roles']

    def create(self, validated_data):
        user: User = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user: User = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
