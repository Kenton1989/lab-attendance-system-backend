from django_filters import rest_framework as filters
from rest_api.models import Week
import logging

log = logging.getLogger(__name__)


class WeekFilter(filters.ModelChoiceFilter):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.get('field_name', '')
        self.lower_bound_lookup = field_name + '__gte'
        self.upper_bound_lookup = field_name + '__lt'
        super().__init__(*args, **kwargs, queryset=Week.objects.all())

    def filter(self, qs, week: Week):
        if (week is None):
            return qs

        qs = self.get_method(qs)(**{
            self.lower_bound_lookup: week.monday,
            self.upper_bound_lookup: week.next_monday,
        })
        return qs.distinct() if self.distinct else qs
