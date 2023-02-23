from django.db.models import Q
from rest_api.models import User, Session, Group
from rest_api.serializers import SessionSerializer
from .common import StaffManagedObjectPermission
from .group import GroupAccessPermission


class SessionAccessPermission(StaffManagedObjectPermission):
    _group_permission = GroupAccessPermission()

    def has_create_object_permission(self, user, request, view, serializer):
        assert isinstance(serializer, SessionSerializer)

        group = serializer.validated_data['group']

        return self._group_permission.has_update_object_permission(
            user, request, view, group)

    def get_managers(self, obj: Session, user_queryset=User.objects.all()):
        return self._group_permission.get_managers(obj.group, user_queryset)

    def get_managed_data(self, user: User, object_queryset=Session.objects.all()):
        groups = self._group_permission.get_managed_data(user)
        return object_queryset.filter(group__in=groups)
