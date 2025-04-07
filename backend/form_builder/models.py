from django.db import models
from django.contrib.postgres.fields import ArrayField
from documents.models import Document


class DocumentForm(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="form")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Form for: '{self.document}' document"


class FormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('tel', 'Phone'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Buttons')
    ]
    form = models.ForeignKey(DocumentForm, on_delete=models.CASCADE, related_name="form_fields")
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    tooltip = models.CharField(max_length=255, default="", blank=True)
    required = models.BooleanField(default=True)
    order = models.IntegerField(default=-1)
    # TODO: writable only on the creation. this should not be modifiable.
    field_id = models.CharField(max_length=255, blank=True)
    choices = ArrayField(
        models.CharField(max_length=255, null=False),
        blank=True, null=True
    )
    
    class Meta:
        ordering = ['order']
        unique_together = ('form', 'field_id')
    
    def save(self, *args, **kwargs):
        # If item was just created, set the order to the highest + 1, so 
        # the new Field gets added to the end of the list automatically, instead of the middle.
        if self.order == -1:
            max_order = FormField.objects.filter(form=self.form).aggregate(models.Max('order'))['order__max']
            self.order = (max_order or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"
