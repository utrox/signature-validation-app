import logging
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from documents.validators import validate_html_extension 


class ValidateHtmlExtensionTests(SimpleTestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_validate_html_file__success(self):
        """Test that a valid HTML file passes validation."""
        file = SimpleUploadedFile("template.html", b"<html>Hello!</html>")
        
        # Should not raise anything
        try:
            validate_html_extension(file)
        except ValidationError:
            self.fail("validate_html_extension() raised ValidationError unexpectedly!")

    def test_validate_non_html_file__rejects(self):
        """Test that a non-HTML file raises ValidationError."""
        file = SimpleUploadedFile("script.js", b"console.log('yo');")
        with self.assertRaises(ValidationError) as context:
            validate_html_extension(file)
        self.assertIn('Only .html files are allowed.', str(context.exception))
