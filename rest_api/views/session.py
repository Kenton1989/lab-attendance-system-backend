from django_filters import rest_framework as filters
from rest_api.models import Session, Lab
from rest_api.serializers import SessionSerializer
from .base import BaseModelViewSet
from .filters import WeekFilter


class SessionFilterSet(filters.FilterSet):
    lab = filters.ModelChoiceFilter(
        field_name='group__lab',
        queryset=Lab.objects.all(),
    )

    start_datetime = filters.IsoDateTimeFromToRangeFilter()
    week = WeekFilter(field_name='start_datetime')

    class Meta:
        model = Session
        fields = ('group', 'is_active',)


class SessionViewSet(BaseModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SessionFilterSet
