from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings  

from signatures.models import Signature  
from users.models import UserProfile, Address
  

User = get_user_model()


class SignatureVerificationTest(TestCase):  
    def setUp(self):  
        # Create a user and thier profile  
        self.address = Address.objects.create(  
            address="123 Test St",  
            city="Test City",  
            zipcode="1234",  
            country="Test Country"  
        )  
          
        self.user_profile = UserProfile.objects.create(  
            first_name="Test",  
            last_name="User",  
            address=self.address,  
            phone="+36 30 234 5678",  
            date_of_birth="1990-01-01",  
            bank_account_number="12345678901234567890"  
        )  
          
        self.user = User.objects.create_user(  
            username="testuser",  
            email="test@example.com",  
            password="testpassword",  
            profile=self.user_profile  
        )  
          
        # Create some stored signatures for the user  
        [
            Signature.objects.create(  
                user=self.user,  
                file=None,  
                features=b'fake_features',  
                time_ms=i * 250,  
            ) for i in range(settings.REGISTRATION_SIGNATURES_COUNT)
        ]
      
    @patch('signatures.models.Signature.compare_signature')  
    def test_verify_signature_success(self, mock_compare):  
        """Test successful signature verification"""  
        # Mock the compare_signature method to return a higher than threshold similarity score  
        mock_compare.return_value = settings.SIGNATURE_SIMILARITY_THRESHOLD + 0.05
          
        # Create a test signature instance  
        test_signature = MagicMock()  
        test_signature.time_ms = 1100  # Similar to stored signatures  
          
        # Verify the signature, assert that the compare_signature method was called 10 times
        # and that the result is None (indicating success)
        result = self.user_profile.verify_signature(test_signature)  
        self.assertIsNone(result)  
        self.assertEqual(mock_compare.call_count, 10)  
      
    @patch('signatures.models.Signature.compare_signature')  
    def test_verify_signature_too_slow(self, mock_compare):  
        """Test signature verification fails when signature is drawn too slowly"""  
        # Create a test signature instance that's way too slow  
        test_signature = MagicMock()  
        test_signature.time_ms = 50000  
          
        # Verify the signature. It should not call the compare_signature method, as the time is too slow
        result = self.user_profile.verify_signature(test_signature)  
        self.assertEqual(result, "Please sign your signature more dynamically.")  
        mock_compare.assert_not_called()  
      
    @patch('signatures.models.Signature.compare_signature')  
    def test_verify_signature_not_matching(self, mock_compare):  
        """Test signature verification fails when signature doesn't match"""  
        # Mock the compare_signature method to return a lower similarity score  
        mock_compare.return_value = settings.SIGNATURE_SIMILARITY_THRESHOLD - 0.05  
          
        # Create a test signature instance  
        test_signature = MagicMock()  
        test_signature.time_ms = 1100  # Similar to stored signatures  
          
        # Verify the signature. It should call the compare_signature method 10 times, 
        # and return an appropriate error message about the signature failing the validation
        result = self.user_profile.verify_signature(test_signature)  
        self.assertEqual(result, "Signature does not match your valid signatures.")  
        self.assertEqual(mock_compare.call_count, 10)
