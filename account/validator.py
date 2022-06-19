from django.core.exceptions import ValidationError


def contact_number_validator(value):
    if value.startswith("01"):
        return value
    return ValidationError("Contact number must be valid!")
