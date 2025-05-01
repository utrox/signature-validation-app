from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock
from django.conf import settings

from signatures.models import Signature
from core.exceptions import UnauthorizedException, NotFoundException
from users.views import me_view, UserProfileView
from users.models import UserProfile, Address

User = get_user_model()


class UserTestsBase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.address = Address.objects.create(
            address="123 Test St",
            city="Test City",
            zipcode="1234",
            country="Test Country",
        )

        self.profile = UserProfile.objects.create(
            first_name='Test',
            last_name='User',
            address=self.address,
            phone='1234567890',
            date_of_birth='1990-01-01',
            bank_account_number='123456789'
        )

        self.user = User.objects.create_user(
            profile = self.profile,
            username='testuser',
            password='testpass',
            is_staff=True  # Admin user for testing
        )

        for i in range(settings.REGISTRATION_SIGNATURES_COUNT):
            Signature.objects.create(
                user=self.user,
                file=None,
                features=b'fake_features',
                time_ms=i * 100,
            )


class UserMeViewTests(UserTestsBase):
    def test_me_view_unauthenticated__returns_null(self):
        """Test that the me_view returns null for unauthenticated users."""
        request = self.factory.get('/me')
        request.user = MagicMock(is_authenticated=False)

        response = me_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 'null')

    def test_me_view_authenticated__success(self):
        """Test that the me_view returns user data for authenticated users."""
        # Mocking user, because we cannot only mock the User model's
        # .signatures.all() method. Django will not allow that and throw an exception:
        # 'TypeError: Direct assignment to the reverse side of a related set is prohibited.'

        request = self.factory.get('/me')
        request.user = self.user
        response = me_view(request)

        self.assertEqual(response.status_code, 200)
        
        expected_response = {
            "is_admin": True,
            "is_signatures_recorded": True
        }
        self.assertJSONEqual(response.content, expected_response)


class UserProfileDetailsViewTests(UserTestsBase):
    def test_user_profile_view_without_login__unauthenticated(self):
        """Test that the user profile view raises exception for unauthenticated users."""
        view = UserProfileView.as_view()

        request = self.factory.get('/profile')
        request.user = MagicMock(is_authenticated=False)

        with self.assertRaises(UnauthorizedException):
            view(request)
    
    def test_user_profile_view_without_profile__not_found(self):
        """Test that the user profile view raises NotFoundException if the user does not have a profile."""
        view = UserProfileView.as_view()

        another_user = User.objects.create_user(username='otheruser', password='testpass', is_staff=True)
        request = self.factory.get('/profile')
        request.user = another_user

        with self.assertRaises(NotFoundException):
            view(request)

    def test_user_profile_view__success(self):
        """Test that the user profile view returns user profile data for authenticated users."""
        view = UserProfileView.as_view()

        request = self.factory.get('/profile')
        request.user = self.user

        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
