import io
from PyPDF2 import PdfReader

from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from documents.generator import generate_pdf, generate_pdf_response
from documents.models import Document


User = get_user_model()


class GeneratorIntegrationTests(TestCase):
    def setUp(self):
        # Create a real document object
        self.document = Document.objects.create(
            name="Test Document",
            template="documents/tests/data/test_template.html",
            is_active=True
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword"
        )

        # Create a context with user data and form data
        self.context = {
            "user": self.user,
            "form_data": {
                "name": "John Doe",
                "address": "123 Test St",
                "phone": "555-1234"
            },
            "preview": True
        }

    def test_generate_pdf_creates_real_pdf(self):
        """Integration test for PDF generation integration with Weasyprint, and that data from context does get added."""
        pdf_content = generate_pdf(self.document.id, self.context)
        text = PdfReader(io.BytesIO(pdf_content)).pages[0].extract_text()

        # Check that we actually got some binary PDF data back
        self.assertIsInstance(pdf_content, bytes)

        # Get text out of PDF, make sure the data from the user, and context did get inserted
        self.assertIn("test@test.com", text)
        self.assertIn("John Doe", text)
        self.assertIn("PREVIEW", text)


    def test_generate_pdf_response_returns_http_response(self):
        """Test application/pdf response does get generated correctly."""
        
        response = generate_pdf_response(self.document.id, self.context)
        pdf_content = response.content
        text = PdfReader(io.BytesIO(pdf_content)).pages[0].extract_text()

        # It does return a PDF response
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Content-Disposition'], 'inline; filename=generated.pdf')
        
        # Get text out of PDF, make sure the data from the user, and context did get inserted
        self.assertIn("test@test.com", text)
        self.assertIn("John Doe", text)
        self.assertIn("PREVIEW", text)