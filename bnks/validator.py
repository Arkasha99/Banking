from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_none(value):
    if value is None:
        raise ValidationError(
            _('%(value)s cannot be null'),
            params={'value': value},
        )
