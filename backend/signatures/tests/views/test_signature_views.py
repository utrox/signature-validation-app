from unittest.mock import patch, MagicMock   

from django.urls import reverse  
from django.conf import settings  
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase  
from rest_framework import status  

from signatures.models import Signature  


User = get_user_model()
BASE_64_IMG_STRING = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuMvu8A7YAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAAYAAAAAEAAABgAAAAAQAAAFBhaW50Lk5FVCA1LjEuMgADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAADp1fY4ytpsegAAADVJREFUOE9jGAU4wX8oDQPofDhggtJkg4E3YHABnCGNBlDUDXwgMkJpECDWCyCArG9AAQMDAGtYBQhykQLeAAAAAElFTkSuQmCC"


class RegisterSignatureViewTest(APITestCase):  
    def setUp(self):  
        # Create a test user  
        self.user = User.objects.create_user(  
            username="testuser",  
            email="test@example.com",  
            password="testpassword"  
        )  
          
        self.url = reverse('register_signatures')  
          
        # Force authenticate the user  
        self.client.force_authenticate(user=self.user)  
          
        # Lower the required signature count, so tests can run a bit faster...  
        self.original_count = settings.REGISTRATION_SIGNATURES_COUNT  
        settings.REGISTRATION_SIGNATURES_COUNT = 3  
          
        # Sample signature data  
        self.signature_data_valid = [  
            {  
                "imgData": BASE_64_IMG_STRING, 
                "signatureTimeMs": 1000  
            },  
            {  
                "imgData": BASE_64_IMG_STRING,  
                "signatureTimeMs": 1200  
            },  
            {  
                "imgData": BASE_64_IMG_STRING,  
                "signatureTimeMs": 1100  
            }  
        ]  
      
    def tearDown(self):  
        # Restore the original signature count. 
        settings.REGISTRATION_SIGNATURES_COUNT = self.original_count  
        super().tearDown()

    # We have to patch the ListSerializer's save method, because we are using 
    # many=True in the serializer. This means that the save method is actually called on
    # the ListSerializer, not the SignatureSerializer class. 
    @patch('rest_framework.serializers.ListSerializer.save')
    def test_register_signatures__success(self, mock_save):  
        """Test successful signature registration"""  
        # Make the request  
        response = self.client.post(self.url, self.signature_data_valid, format='json')  
          
        # Check response, and that the save was called  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(response.data['message'], "Signatures registered successfully")  
        mock_save.assert_called_once()  
      
    def test_register_signatures_too_few__bad_request(self):  
        """Test that exactly the required number of signatures must be provided - too few."""  
        # Remove one signature  
        data = self.signature_data_valid[:-1]  
          
        # Make the request  
        response = self.client.post(self.url, data, format='json')  
          
        # Check that we get a validation error  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        self.assertIn(f"Exactly {settings.REGISTRATION_SIGNATURES_COUNT} signatures are required", str(response.data))  
    
    def test_register_signatures_too_many__bad_request(self):
        """Test that exactly the required number of signatures must be provided - too many."""  
        # Add one more signature  
        data = self.signature_data_valid + [self.signature_data_valid[0]]  
          
        # Make the request  
        response = self.client.post(self.url, data, format='json')  
          
        # Check that we get a validation error  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        self.assertIn(f"Exactly {settings.REGISTRATION_SIGNATURES_COUNT} signatures are required", str(response.data))

    def test_register_signatures_already_registered__bad_request(self):  
        """Test that users can't register signatures twice"""  
        # Create existing signatures  
        for i in range(settings.REGISTRATION_SIGNATURES_COUNT):  
            Signature.objects.create(  
                user=self.user,  
                time_ms=1000 + i * 100  
            )  
          
        # Make the request and try to register the signatures again
        response = self.client.post(self.url, self.signature_data_valid, format='json')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        self.assertIn("You've already registered your signatures", str(response.data))  
      
    def test_register_signatures_empty_data__bad_request(self):  
        """Test that empty data returns a 400 error"""  
        # Make the request with empty data  
        response = self.client.post(self.url, {}, format='json')  
          
        # Check that we get a validation error  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        self.assertIn("Exactly 3 signatures are required", str(response.data))
    
    def test_register_signatures_not_base64__bad_request(self):
        """Test that uplodaing a non-base64 signature image data returns a 400 error"""
        # Modify a base64 string to be invalid
        invalid_base64_string = "data:image/png;base64,invalid_base64_string"
        self.signature_data_valid[0]["imgData"] = invalid_base64_string
        
        # Make the request and check that we get a validation error
        response = self.client.post(self.url, self.signature_data_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid Base64-encoded image data", str(response.data))