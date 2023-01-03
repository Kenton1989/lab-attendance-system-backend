from django.contrib.auth.models import Group as AuthGroup
from .base import BaseModelSerializer
from rest_framework.serializers import IntegerField, CharField
from rest_framework.exceptions import ValidationError


class AuthGroupSerializer(BaseModelSerializer):
    class Meta:
        model = AuthGroup
        fields = ['id', 'name',]


class AuthGroupWithWritableIdSerializer(BaseModelSerializer):
    '''Special serializer used to handle relationship between user and auth-group.

    `id` is allowed to appeared in writing operations for the following reason.

    For two write operation:
    - create: `id` can be used to look for existing group to create relationship.
    - update: updating any auth group through relationship is forbidden.

    Therefore, `id` is needed for some writing operation
    '''
    id = IntegerField(read_only=False, write_only=False, required=False)
    name = CharField(read_only=False, write_only=False, required=False)

    def validate(self, attrs):
        if not 'id' in attrs and not 'name' in attrs:
            raise ValidationError('either "id" or "name" must be provided')

    class Meta(AuthGroupSerializer.Meta):
        model = AuthGroup
        fields = ['id', 'name',]
