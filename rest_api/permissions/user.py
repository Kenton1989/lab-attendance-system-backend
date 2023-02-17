from rest_api.models import User
from .common import StaffManagedObjectPermission, is_superuser, is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.serializers import Serializer, ListSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Model

import logging

log = logging.getLogger(__name__)


class UserAccessPermission(StaffManagedObjectPermission):
    """
    Permission about User model.
    """

    def get_managed_data(self, user: User, object_queryset=User.objects.all()):
        # a user can update his own user object.
        return object_queryset.filter(pk=user.id)

    def get_managers(self, obj: User, user_queryset=User.objects.all()):
        # user object can be updated by the user it represents.
        return user_queryset.filter(pk=obj.id)

    # The user can only update a limited set of field
    USER_SELF_WRITABLE_FIELDS = ('password', 'email')

    @classmethod
    def scope_fields(cls, request: Request, serializer: Serializer) -> Serializer:
        """
        Update the read_only/write_only of serializer.fields to achieve field-level permission control.

        This is not a method defined by Django/Django REST Framework, therefore it will not be automatically called.
        Please make sure it is explicitly called somewhere, likely in a method overriding GenericAPIView.get_serializer.
        """
        # superuser can do anything
        if is_superuser(request.user):
            return serializer

        instance: User = serializer.instance

        if (instance is not None and
            isinstance(instance, User) and
            instance.id == request.user.id and
                cls.USER_SELF_WRITABLE_FIELDS is not None):
            # user can update a limited set of fields of his own user object
            writable_fields = cls.USER_SELF_WRITABLE_FIELDS
        else:
            # all the other case are read-only
            writable_fields = tuple()

        if isinstance(serializer, ListSerializer):
            fields = serializer.child.fields
        else:
            fields = serializer.fields

        readonly_fields = (set(fields.keys())
                           .difference(writable_fields))

        for field_name in readonly_fields:
            field = fields.get(field_name)
            if field.write_only:
                # remove write-only fields
                fields.pop(field_name)
            elif not field.read_only:
                # make read-write field read-only
                field.read_only = True

        return serializer


class UserRelationshipReadOnlyAccessPermission(BasePermission):
    '''
    Permission about read-only data related to an user.
    Grant read access to superuser and the related user.
    '''
    user_url_lookup_kwarg = 'user_pk'

    def has_permission(self, request: Request, view: ViewSet):
        if request.method not in SAFE_METHODS:
            return False

        if not is_authenticated(request.user):
            return False

        if is_superuser(request.user):
            return True

        assert self.user_url_lookup_kwarg in view.kwargs, (
            f'expecting "{self.user_url_lookup_kwarg}" in `view.kwargs` '
            'please check URL config or change `.user_url_lookup_kwarg`.'
        )

        user_id = view.kwargs[self.user_url_lookup_kwarg]

        if user_id == settings.USER_SELF_ID:
            return True

        queried_user = get_object_or_404(User, pk=user_id)

        return queried_user.id == request.user.id
