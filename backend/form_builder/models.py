from django.db import models

from documents.models import Document
from django.contrib.postgres.fields import ArrayField


class DocumentForm(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="form")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Form for: '{self.document}' document"


class FormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('date', 'Date'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        ('file', 'File Upload'),
        ('radio', 'Radio Buttons')
    ]
    form = models.OneToOneField(DocumentForm, on_delete=models.CASCADE, related_name="form_fields")
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    choices = ArrayField(
        models.CharField(max_length=255, null=False),
        blank=True, null=True
    )
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"
