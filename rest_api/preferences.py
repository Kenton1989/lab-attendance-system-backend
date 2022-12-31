from dynamic_preferences.types import IntegerPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from django.core.exceptions import ValidationError

session = Section('session')


@global_preferences_registry.register
class EarliestCheckInMinutes(IntegerPreference):
    section = session
    name = 'earliest_check_in_minutes'
    default = 15
    required = False

    def validate(self, value):
        if value < 0:
            raise ValidationError(
                'earliest_check_in_minutes must be greater or equal then 0')


preferences = global_preferences_registry.manager()
