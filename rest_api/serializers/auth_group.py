from django.contrib.auth.models import Group
from .base import BaseModelSerializer


class AuthGroupSerializer(BaseModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name',]
