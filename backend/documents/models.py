from django.db import models
from .validators import validate_html_extension 

# Create your models here.
class Document(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    # TODO: error handling in PDF preview: if the .html file is invalid or smth, and throws an error when generated.
    template = models.FileField(upload_to='document_templates/', validators=[validate_html_extension])
