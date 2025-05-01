import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from .authentication_test_base_class import AuthenticationViewsTestsBase


User = get_user_model()


class TestRegisterViews(AuthenticationViewsTestsBase):
    def test_login__successful(self):
        """Test login with valid credentials"""
        response = self.client.post(
            reverse('login_view'),
            data=json.dumps({'username': self.user.username, 'password': self.user_password}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)  # Redirect on success
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials__unauthorized(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            reverse('login_view'),
            data=json.dumps({'username': self.user.username, 'password': 'wrongpassword'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)  # Unauthorized
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_empty_body__bad_request(self):
        """Test login with empty body"""
        response = self.client.post(reverse('login_view'), data='', content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_json__bad_request(self):
        """Test login with invalid JSON"""
        response = self.client.post(reverse('login_view'), data='invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_login_missing_fields__bad_request(self):
        """Test login with missing fields"""
        response = self.client.post(
            reverse('login_view'),
            data=json.dumps({'username': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    