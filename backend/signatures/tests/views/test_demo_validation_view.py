import pickle
import numpy as np
from unittest.mock import patch, MagicMock

from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from signatures.models import Signature
from users.models import UserProfile, Address


User = get_user_model()
BASE_64_IMG_STRING = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuMvu8A7YAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAAYAAAAAEAAABgAAAAAQAAAFBhaW50Lk5FVCA1LjEuMgADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAADp1fY4ytpsegAAADVJREFUOE9jGAU4wX8oDQPofDhggtJkg4E3YHABnCGNBlDUDXwgMkJpECDWCyCArG9AAQMDAGtYBQhykQLeAAAAAElFTkSuQmCC"


class DemoVerifySignatureViewTest(APITestCase):  
    def setUp(self):  
        # Create a test user with profile  
        self.address = Address.objects.create(  
            address="123 Test St",  
            city="Test City",  
            zipcode="12345",  
            country="Test Country"  
        )  
          
        self.user_profile = UserProfile.objects.create(  
            first_name="Test",  
            last_name="User",  
            address=self.address,  
            phone="+1 234 5678",  
            date_of_birth="1990-01-01",  
            bank_account_number="12345678901234567890"  
        )  
          
        self.user = User.objects.create_user(  
            username="testuser",  
            email="test@example.com",  
            password="testpassword",  
            profile=self.user_profile  
        )  
          
        # URL for verifying signatures  
        self.url = reverse('demo_verification')  
          
        # Authenticate the user  
        self.client.force_authenticate(user=self.user)  
          
        # Create some stored signatures for the user  
        for i in range(3):  
            Signature.objects.create(  
                user=self.user,  
                time_ms=1000 + i * 100,  
                features=pickle.dumps(np.random.rand(1, 1280))  # Random features  
            )  
          
        # Sample signature data for verification  
        self.signature_data = {  
            "imgData": BASE_64_IMG_STRING,  
            "signatureTimeMs": 1100  
        }  

        self.original_count = settings.REGISTRATION_SIGNATURES_COUNT
        settings.REGISTRATION_SIGNATURES_COUNT = 3
    
    def tearDown(self):  
        # Restore the original signature count. 
        settings.REGISTRATION_SIGNATURES_COUNT = self.original_count
        super().tearDown()
      
    @patch('signatures.serializers.SignatureSerializer.model_instance')  
    @patch('users.models.UserProfile.verify_signature')  
    def test_verify_signature_success(self, mock_verify, mock_model_instance):  
        """Test successful signature verification"""  
        # Mock the model_instance method to return a signature instance  
        mock_signature = MagicMock()  
        mock_model_instance.return_value = mock_signature  
          
        # Mock verify_signature to return None (success)  
        mock_verify.return_value = None  
          
        # Make the request and check the response
        response = self.client.post(self.url, self.signature_data, format='json')  
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.data['message'], "Signature verified!")  
          
        # Check that verify_signature was called with the signature instance  
        mock_verify.assert_called_once_with(mock_signature)  
      
    @patch('signatures.serializers.SignatureSerializer.model_instance')  
    @patch('users.models.UserProfile.verify_signature')  
    def test_verify_signature_failure(self, mock_verify, mock_model_instance):  
        """Test failed signature verification"""  
        # Mock the model_instance method to return a signature instance  
        mock_signature = MagicMock()  
        mock_model_instance.return_value = mock_signature  
          
        # Mock verify_signature to return an error message  
        error_message = "Signature does not match your valid signatures."  
        mock_verify.return_value = error_message  
          
        # Make the request  
        response = self.client.post(self.url, self.signature_data, format='json')  
          
        # Check that we get a bad request error with the error message  
        self.assertEqual(response.status_code, 400)  
      
    def test_verify_signature_unauthenticated(self):  
        """Test that unauthenticated users cannot verify signatures"""  
        # Unauthenticate the client  
        self.client.force_authenticate(user=None)  
          
        # Make the request and check that we get an unauthorized error
        response = self.client.post(self.url, self.signature_data, format='json')  
        self.assertEqual(response.status_code, 403)  
      
    def test_verify_signature_invalid_data(self):  
        """Test handling invalid signature data"""  
        # Invalid data missing required fields  
        invalid_data = {  
            "signatureTimeMs": 1100  
            # Missing imgData  
        }  
          
        # Make the request and check we get a validation error
        response = self.client.post(self.url, invalid_data, format='json')  
        self.assertEqual(response.status_code, 400)
