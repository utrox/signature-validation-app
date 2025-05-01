from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User
from documents.models import Document
from signatures.models import Signature
from signature_workflows.models import SignatureWorkflow


class SignatureWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        
        [Signature.objects.create(
            user=self.user,
            file=None,
            features=b'fake_features',
            time_ms=100,
        ) for _ in range(10)]

        self.document = Document.objects.create(name='Test Document', is_active=True, template='test.html')

    def test_create_signature_workflow__success(self):
        """Test that a signature workflow can be created successfully with valid data."""
        self.client.force_authenticate(user=self.user)

        url = reverse('workflows')
        data = {
            "document_id": str(self.document.id),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)

    def test_create_signature_workflow_without_login__unauthenticated(self):
        """Test that creating a signature workflow without authentication returns 403."""
        url = reverse('workflows')
        data = {
            "document": str(self.document.id),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
    
    def test_create_signature_workflow_without_signatures__unauthorized(self):
        """Test that creating a signature workflow without signatures returns 403."""
        self.client.force_authenticate(user=self.user2)
        url = reverse('workflows')
        data = {
            "document": str(self.document.id),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
