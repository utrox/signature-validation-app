from django.core.exceptions import ValidationError


def validate_html_extension(value):
        if not value.name.endswith('.html'):
            raise ValidationError('Only .html files are allowed.')
