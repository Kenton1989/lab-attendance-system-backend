from .base import BaseModelViewSet
from rest_api.serializers import AuthGroupSerializer
from django.contrib.auth.models import Group as AuthGroup
from rest_api.permissions import IsSuperuserOrAuthenticatedReadOnly


class RoleViewSet(BaseModelViewSet):
    queryset = AuthGroup.objects.all()
    serializer_class = AuthGroupSerializer

    permission_classes = (IsSuperuserOrAuthenticatedReadOnly, )
