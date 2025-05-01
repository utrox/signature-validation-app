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

    def test_list_signature_workflows__success(self):
        """Test that listing signature workflows returns a list of workflows."""
        self.client.force_authenticate(user=self.user)

        SignatureWorkflow.objects.create(document=self.document, user=self.user)
        url = reverse('workflows')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_signature_workflows_without_login__unauthenticated(self):
        """Test that listing signature workflows without authentication returns 403."""
        url = reverse('workflows')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_list_signature_workflows_without_signatures__unauthorized(self):
        """Test that listing signature workflows without the user having signatures recorded makes the request unauthorized."""
        self.client.force_authenticate(user=self.user2)
        url = reverse('workflows')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    