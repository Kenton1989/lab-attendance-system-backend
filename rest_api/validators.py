from django.core.exceptions import ValidationError
import re
from datetime import date

_username_pattern = re.compile(r'^\w+$')

def username_validator(value: str) -> None:
    if not _username_pattern.match(value):
        raise ValidationError(
            'The username can only cantains alphabets and digits.')

_monday_code = 0
def monday_validator(value: date) -> None:
    if value.weekday() != _monday_code:
        raise ValidationError(
            'The date is not monday.')
