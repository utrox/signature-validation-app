from django.http import Http404
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, force_authenticate

from core.exceptions.exceptions import BadRequestException
from documents.models import Document
from form_builder.models import DocumentForm, FormField
from signature_workflows.models import SignatureWorkflow
from signature_workflows.serializer import SignatureWorkflowCreateSerializer


User = get_user_model()


class SignatureWorkflowCreateSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user2 = User.objects.create_user(username='testuser2', password='password2')
        self.document = Document.objects.create(name="Test Doc", template="template.html")
        self.form = DocumentForm.objects.create(document=self.document, description="Test form")
        self.required_field = FormField.objects.create(
            form=self.form,
            label="Required Field",
            field_type="text",
            required=True,
            field_id="required_field"
        )
        self.optional_field = FormField.objects.create(
            form=self.form,
            label="Optional Field",
            field_type="text",
            required=False,
            field_id="optional_field"
        )
        self.request_context = {'request': self._mock_request(self.user)}

    def _mock_request(self, user):
        factory = APIRequestFactory()
        raw_request = factory.post('/fake-url/')
        force_authenticate(raw_request, user=user)
        return Request(raw_request)


    def test_valid_data_creates_workflow__success(self):
        """Test that valid data creates a SignatureWorkflow instance."""
        data = {
            "document_id": self.document.id,
            "form_data": {
                "required_field": "Some value",
                "optional_field": "Optional value"
            }
        }

        # We use the serializer to validate and create the instance
        serializer = SignatureWorkflowCreateSerializer(data=data, context=self.request_context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        # Assert that the instance is created correctly
        self.assertIsInstance(instance, SignatureWorkflow)
        self.assertEqual(instance.document, self.document)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.form_data["required_field"], "Some value")
        self.assertEqual(instance.form_data["optional_field"], "Optional value")

    def test_missing_required_field__bad_request(self):
        """Test that missing required field raises BadRequestException."""
        data = {
            "document_id": self.document.id,
            "form_data": {
                "optional_field": "Optional value"
            }
        }

        serializer = SignatureWorkflowCreateSerializer(data=data, context=self.request_context)
        with self.assertRaises(BadRequestException):
            serializer.is_valid(raise_exception=True)

    def test_missing_form_data_when_required__bad_request(self):
        """Test that missing form data when form is required raises BadRequestException."""
        data = {
            "document_id": self.document.id,
        }

        serializer = SignatureWorkflowCreateSerializer(data=data, context=self.request_context)
        with self.assertRaises(BadRequestException):
            serializer.is_valid(raise_exception=True)

    def test_valid_data_when_form_not_required__success(self):
        """Test that valid data when form is not required creates a SignatureWorkflow instance."""
        doc_without_form = Document.objects.create(name="No Form Doc", template="template2.html")
        
        data = {
            "document_id": doc_without_form.id,
        }
        
        serializer = SignatureWorkflowCreateSerializer(data=data, context=self.request_context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        self.assertIsInstance(instance, SignatureWorkflow)
        self.assertEqual(instance.document, doc_without_form)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.form_data, {})

    def test_invalid_document_id__not_found(self):
        """Test that invalid document ID raises Http404."""
        data = {
            "document_id": 9999,
            "form_data": {
                "required_field": "Value"
            }
        }
        
        serializer = SignatureWorkflowCreateSerializer(data=data, context=self.request_context)
        with self.assertRaises(Http404):
            serializer.is_valid(raise_exception=True)
