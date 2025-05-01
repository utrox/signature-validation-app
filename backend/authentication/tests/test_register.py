import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from .authentication_test_base_class import AuthenticationViewsTestsBase

User = get_user_model()


class TestRegisterView(AuthenticationViewsTestsBase):
    def test_register_empty_body__bad_request(self):
        """Test register with empty body"""
        response = self.client.post(reverse('register_view'), data='', content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_register_invalid_json__bad_request(self):
        """Test register with invalid JSON"""
        response = self.client.post(reverse('register_view'), data='invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_register_missing_fields__bad_request(self):
        """Test register with missing fields"""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'email': 'asd@asd.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_register_invalid_password_short__bad_request(self):
        """Test register with password too short."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'password': 'Asztal2', 'email': 'asd@asd.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_register_invalid_password_numeric__bad_request(self):
        """Test register with password without letters."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'password': '12345678', 'email': 'asd@asd.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_register_invalid_password_common__bad_request(self):
        """Test register with password too common."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'password': 'Password123', 'email': 'asd@asd.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_register_duplicate_username__conflict(self):
        """Test register with duplicate username."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': self.user.username, 'password': 'StrongP@ssw0rd', 'email': 'asd@asd.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)  # Conflict

    def test_register_missing_email__bad_request(self):
        """Test register with missing email."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'password': 'StrongP@ssw0rd'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400) 
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_register_invalid_email_format__bad_request(self):
        """Test register with invalid email format."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'password': 'StrongP@ssw0rd', 'email': 'invalid-email'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_register__successful(self):
        """Test register with valid data."""
        response = self.client.post(
            reverse('register_view'),
            data=json.dumps({'username': 'newuser', 'password': 'StrongP@ssw0rd', 'email': 'asd@asd.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)  # Redirects on success
        self.assertTrue(User.objects.filter(username='newuser').exists())
