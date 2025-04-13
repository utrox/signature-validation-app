from django.db import models
from simple_history.models import HistoricalRecords

from .validators import validate_html_extension 

# Create your models here.
class Document(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    template = models.FileField(upload_to='document_templates/', validators=[validate_html_extension])
    history = HistoricalRecords()

    @property
    def requires_form_for_submission(self):
        """
        Check if the document requires formdata for submission.
        """
        return hasattr(self, 'form') and (
            hasattr(self.form, 'form_fields') and 
            self.form.form_fields.exists()
        )

    def __str__(self):
        return self.name
