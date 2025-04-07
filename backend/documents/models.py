from django.db import models
from .validators import validate_html_extension 

# Create your models here.
class Document(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    template = models.FileField(upload_to='document_templates/', validators=[validate_html_extension])

    @property
    def requires_form_for_submission(self):
        """
        Check if the document requires formdata for submission.
        """
        # TODO: check (in a different method/property) if all required fields are present in the form data.
        return hasattr(self, 'form') and (
            hasattr(self.form, 'form_fields') and 
            self.form.form_fields.exists()
        )

    def __str__(self):
        return self.name
