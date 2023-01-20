from .base import BaseModelViewSet
from rest_api.serializers import AuthGroupSerializer
from django.contrib.auth.models import Group as AuthGroup
from rest_api.permissions import IsSuperuserOrAuthenticatedReadOnly
from .schemas import RoleSchema


class RoleViewSet(BaseModelViewSet):
    schema = RoleSchema()

    queryset = AuthGroup.objects.all()
    serializer_class = AuthGroupSerializer

    permission_classes = (IsSuperuserOrAuthenticatedReadOnly, )
