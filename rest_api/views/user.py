from rest_framework.filters import SearchFilter
from .base import BaseModelViewSet
from rest_api.serializers import UserSerializer
from rest_api.models import User
from rest_api.permissions import UserAccessPermission
from django_filters import rest_framework as filters
from django.contrib.auth.models import Group as AuthGroup
from django.conf import settings


class UserFilterSet(filters.FilterSet):
    roles_contain = filters.ModelChoiceFilter(
        field_name="groups",
        queryset=AuthGroup.objects.all(),
    )

    role_names_contain = filters.CharFilter(field_name='groups__name')

    class Meta:
        model = User
        fields = ('is_active',)


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    search_fields = ('username', 'display_name',)
    filterset_class = UserFilterSet

    permission_classes = (UserAccessPermission, )

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk == settings.USER_SELF_ID:
            self.kwargs['pk'] = self.request.user.id
        return super().get_object()

    def get_serializer(self, *args, **kwargs):
        res = super().get_serializer(*args, **kwargs)
        res = UserAccessPermission.scope_fields(self.request, res)
        return res
