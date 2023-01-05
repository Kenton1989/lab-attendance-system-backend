from rest_api.models import User
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_api.permissions import ExtendedObjectPermission, StaffManagedObjectPermission, UserRelationshipReadOnlyAccessPermission
from typing import Type
from django.shortcuts import get_object_or_404


class BaseModelViewSet(ModelViewSet):
    def perform_create(self, serializer):
        self.check_create_object_permissions(self, self.request, serializer)
        return super().perform_create(serializer)

    def check_create_object_permissions(self, request, serializer):
        for perm in self.get_permissions():
            if not isinstance(perm, ExtendedObjectPermission):
                continue

            if perm.has_create_object_permission(request.user, request, self, serializer):
                self.permission_denied(request,
                                       message=getattr(perm, 'message', None),
                                       code=getattr(perm, 'code', None))


class UserRelatedObjectGenericViewSet(GenericViewSet):
    user_url_lookup_kwarg = 'user_pk'

    @property
    def queried_user(self) -> User:
        if not hasattr(self, '_queried_user'):
            user_id = self.get_queried_user_id()
            user = self.get_user_by_id(user_id)
            setattr(self, '_queried_user', user)
        return self._queried_user

    def get_queried_user_id(self):
        assert self.user_url_lookup_kwarg in self.kwargs, (
            f'expecting "{self.user_url_lookup_kwarg}" in `view.kwargs` '
            'please check URL config or change `.user_url_lookup_kwarg`.'
        )

        return self.kwargs[self.user_url_lookup_kwarg]

    def get_user_by_id(self, user_id) -> User:
        if user_id == 'me':
            return self.request.user

        return get_object_or_404(User, pk=user_id)


class UserManagedObjectViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               UserRelatedObjectGenericViewSet):

    management_permission_class: Type[StaffManagedObjectPermission]

    permission_classes = (UserRelationshipReadOnlyAccessPermission, )

    def get_queryset(self):
        management_permission = self.get_management_permission()
        return management_permission.get_managed_data(self.queried_user, super().get_queryset())

    def get_management_permission(self):
        perm = self.management_permission_class()
        return perm
