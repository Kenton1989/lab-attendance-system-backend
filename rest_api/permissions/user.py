from rest_api.models import User, parse_user_id
from .common import StaffManagedObjectPermission, is_superuser, is_authenticated
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import bad_request


class UserAccessPermission(StaffManagedObjectPermission):
    def get_managed_data(self, user: User, object_queryset=User.objects.all()):
        return object_queryset.filter(pk=user.id)

    def get_managers(self, obj: User, user_queryset=User.objects.all()):
        return user_queryset.filter(pk=obj.id)


class UserRelationshipAccessPermission(BasePermission):
    '''
    Grant all access to superuser and user himself 
    '''
    user_url_lookup_kwarg = 'user_pk'

    def has_permission(self, request: Request, view: ViewSet):
        if not is_authenticated(request.user):
            return False

        if is_superuser(request.user):
            return True

        assert self.user_url_lookup_kwarg in view.kwargs, (
            f'expecting "{self.user_url_lookup_kwarg}" in `view.kwargs` '
            'please check URL config or change `.user_url_lookup_kwarg`.'
        )

        user_id_str = view.kwargs[self.user_url_lookup_kwarg]

        user_id = parse_user_id(user_id_str, request)
        if user_id is None:
            return False

        if user_id == request.user:
            return True

        return False