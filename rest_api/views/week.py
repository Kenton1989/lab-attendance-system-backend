from .base import BaseModelViewSet
from rest_framework.exceptions import ValidationError
from rest_api.serializers import WeekSerializer
from rest_api.models import Week
from datetime import datetime


class WeekViewSet(BaseModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer

    def get_queryset(self):
        res = super().get_queryset()
        res = self._contain_timestamp_filter(res)
        return res

    def _contain_timestamp_filter(self, queryset):
        contain_timestamp_str = self.request.query_params.get(
            'contain_timestamp', '')

        if not contain_timestamp_str:
            return queryset

        try:
            contain_timestamp = datetime.fromisoformat(contain_timestamp_str)
        except ValueError as e:
            raise ValidationError(
                {'contain_timestamp': ['invalid ISO 8601 format string']})

        contain_date = contain_timestamp.date()

        queryset = queryset.filter(
            monday__lte=contain_date,
            next_monday__gt=contain_date
        )

        return queryset
