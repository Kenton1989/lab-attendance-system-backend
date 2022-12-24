from rest_framework.viewsets import ModelViewSet
from rest_api.serializers import LabSerializer
from rest_api.models import Lab, User
from django_filters import rest_framework as filters


class LabFilterSet(filters.FilterSet):
    executives_contain = filters.ModelChoiceFilter(
        field_name="executives",
        queryset=User.objects.all(),
    )


class LabViewSet(ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LabFilterSet
