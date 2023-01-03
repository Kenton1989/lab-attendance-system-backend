from .base import BaseModelViewSet
from rest_api.serializers import LabSerializer
from rest_framework.filters import SearchFilter
from rest_api.models import Lab, User
from rest_api.permissions import LabAccessPermission
from django_filters import rest_framework as filters


class LabFilterSet(filters.FilterSet):
    executives_contain = filters.ModelChoiceFilter(
        field_name="executives",
        queryset=User.objects.all(),
    )
    is_active = filters.BooleanFilter(field_name="user__is_active")


class LabViewSet(BaseModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter,)
    search_fields = ('user__username', 'user__display_name',)
    filterset_class = LabFilterSet

    permission_classes = (LabAccessPermission,)
