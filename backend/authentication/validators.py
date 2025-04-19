from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    NumericPasswordValidator,
    CommonPasswordValidator,
)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_password(password: str):
    """Run validators on a password and return a list of errors."""
    validators = [
        MinimumLengthValidator,
        NumericPasswordValidator,
        CommonPasswordValidator,
    ]
    errors = []

    for validator in validators:
        try:
            validator().validate(password)
        except ValidationError as e:
            errors.append(str(e.messages[0]))
    
    # There's no built-in validator for password maximum length, so we'll add it here.
    if len(password) > 32:
        errors.append(ValidationError("Password must be at most 32 characters long."))

    return errors

