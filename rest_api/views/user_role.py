from rest_api.serializers import AuthGroupWithWritableIdSerializer
from django.contrib.auth.models import Group as AuthGroup
from rest_api.permissions import IsSuperuser
from .base import UserRelatedObjectGenericViewSet
from rest_framework import mixins
from rest_framework.exceptions import ValidationError


class UserRoleViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      UserRelatedObjectGenericViewSet):

    queryset = AuthGroup.objects.all()
    serializer_class = AuthGroupWithWritableIdSerializer

    # Only superuser can access this API.
    # Other user can only read user's role through UserViewSet
    permission_classes = (IsSuperuser, )

    def get_queryset(self):
        return super().get_queryset().filter(user_set=self.queried_user)

    def perform_create(self, serializer: AuthGroupWithWritableIdSerializer):
        group_lookup = serializer.validated_data
        added_group = AuthGroup.objects.filter(**group_lookup)
        if not added_group.exists():
            raise ValidationError(
                'group with specified name and id does not exist')
        self.queried_user.groups.add(added_group)

    def perform_destroy(self, instance: AuthGroup):
        self.queried_user.groups.remove(instance)
