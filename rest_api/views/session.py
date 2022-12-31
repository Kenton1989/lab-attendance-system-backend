from .base import BaseModelViewSet
from rest_api.serializers import SessionSerializer
from rest_api.models import Session, Lab
from django_filters import rest_framework as filters


class SessionFilterSet(filters.FilterSet):
    lab = filters.ModelChoiceFilter(
        field_name='group__lab',
        queryset=Lab.objects.all(),
    )

    start_datetime = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Session
        fields = ('group', 'is_active',)


class SessionViewSet(BaseModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
