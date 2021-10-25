from django.core.exceptions import ValidationError
from django.utils import timezone as dt


def year_validator(value):
    if value < 1900 or value > dt.now().year:
        raise ValidationError('%(value)s is not a correct year!',
                              params={'value': value},)
