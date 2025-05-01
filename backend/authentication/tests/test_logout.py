from django.contrib.auth import get_user_model
from django.urls import reverse

from .authentication_test_base_class import AuthenticationViewsTestsBase

User = get_user_model()


class TestLogoutViews(AuthenticationViewsTestsBase):
    def test_logout__successful(self):
        """Test logout when user is authenticated"""
        self.client.force_login(self.user)  # Log in the user first
        response = self.client.post(reverse('logout_view'))
        self.assertEqual(response.status_code, 204)  # Redirects on success
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_unauthenticated__successful(self):
        """Test logout when user is not authenticated"""
        # This is a bit of a weird case, but we want to ensure that
        # this does not causes anything to break or throw an unhandled error.
        response = self.client.post(reverse('logout_view'))
        self.assertEqual(response.status_code, 204)  # Redirects on success
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    