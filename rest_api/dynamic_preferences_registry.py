from dynamic_preferences.types import IntegerPreference, StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from django.core.exceptions import ValidationError

session = Section('session')
server_email = Section('server_email')


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


@global_preferences_registry.register
class ServerEmailAddress(StringPreference):
    section = server_email
    name = 'address'
    default = 'dummy@ntu.edu.sg'
    required = False


@global_preferences_registry.register
class ServerEmailAddress(StringPreference):
    section = server_email
    name = 'password'
    default = 'dummy password'
    required = False


@global_preferences_registry.register
class ServerEmailAddress(StringPreference):
    section = server_email
    name = 'smtp_server'
    default = 'smtp.ntu.edu.sg'
    required = False


preferences = global_preferences_registry.manager()
