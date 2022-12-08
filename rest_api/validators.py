from django.core.exceptions import ValidationError
import re


username_pattern = re.compile(r'^\w+$')

def username_validator(value: str) -> None:
    if not username_pattern.match(value):
        raise ValidationError(
            'The username can only cantains alphabets and digits.')
