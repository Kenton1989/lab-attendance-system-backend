from rest_framework.permissions import BasePermission
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_api.models import User
from django.db.models import QuerySet
from typing import Any


# common user checkers

def is_authenticated(user):
    return user and user.is_authenticated


def is_anonymous(user):
    return user and not user.is_authenticated


def is_superuser(user):
    return is_authenticated(user) and user.is_superuser


def in_group(user, group_name: str):
    return (is_authenticated(user) and
            user.groups.filter(name=group_name).exists())


def with_uid(user, id: int):
    return (is_authenticated(user) and
            user.id == id)


def with_username(user, name: str):
    return (is_authenticated(user) and
            user.username == name)


class ExtendedObjectPermission(BasePermission):
    '''
    Permission class with additional functions to allow define customized object level permission easier. 
    `has_object_permission` is overridden to use this function for permission checking.

    - `has_create_object_permission(self, user: User, request: Request, view: ViewSet, serializer: Serializer) -> bool`
    - `has_retrieve_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool`
    - `has_update_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool`
    - `has_destroy_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool`

    CAUTION: `has_create_object_permission` are not called automatically in the 
    permission system. It needs to be manually integrated into the ViewSet. 
    One possible location is override ViewSet.perform_create to check permission before creation.
    '''

    def has_object_permission(self, request, view, obj):
        action = view.action

        if action == 'retrieve':
            return self.has_retrieve_object_permission(request.user, request, view, obj)

        if action in {'update', 'partial_update'}:
            return self.has_update_object_permission(request.user, request, view, obj)

        if action == 'destroy':
            return self.has_destroy_object_permission(request.user, request, view, obj)

        return True

    def has_create_object_permission(self, user: User, request: Request, view: ViewSet, serializer: Serializer) -> bool:
        return True

    def has_retrieve_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool:
        return True

    def has_update_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool:
        return True

    def has_destroy_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool:
        return True


class StaffManagedObjectPermission(ExtendedObjectPermission):
    '''A permission template used for various data types.

    Details:
    - superuser is allowed to perform any operations.
    - retrieve: allowed for all authenticated user.
    - list: allowed for user in `staff` group.
    - update/partial_update: require user in `staff` group and 
      `self.has_update_object_permission(user, request, view, object)` is True. 
      `has_update_object_permission` call `get_managers` to check if user is the manager of object.
    - create: requires user in `staff` group and
      `self.has_create_object_permission(user, request, view, serializer)` is True. 
      It will return False by default.
    - destroy: not allowed for any user except superuser.
    '''

    def has_permission(self, request: Request, view: ViewSet):
        user = request.user
        if not is_authenticated(user):
            return False

        if is_superuser(user):
            return True

        action = view.action

        if action == 'retrieve':
            return True

        if action in {'list', 'create', 'update', 'partial_update'}:
            return in_group(user, 'staff')

        return False

    def has_object_permission(self, request, view, obj):
        if is_superuser(request.user):
            return True

        return super().has_object_permission(request, view, obj)

    def has_create_object_permission(self, user: User, request: Request, view: ViewSet, serializer: Serializer) -> bool:
        return False

    def has_retrieve_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool:
        return True

    def has_update_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool:
        return self.get_managers(obj).filter(pk=user.id).exists()

    def has_destroy_object_permission(self, user: User, request: Request, view: ViewSet, obj: Any) -> bool:
        return False

    def get_managed_data(self, user: User, object_queryset: QuerySet = None) -> QuerySet:
        raise NotImplementedError('get_managed_data is not implemented')

    def get_managers(self, obj: Any, user_queryset: QuerySet = User.objects.all()) -> QuerySet:
        return user_queryset.none()


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return is_superuser(user)
