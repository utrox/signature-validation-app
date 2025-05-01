import pickle
import numpy as np
import base64
from io import BytesIO
from django.test import TestCase
from unittest.mock import patch, MagicMock
from PIL import Image, ImageDraw

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from signatures.encoder import preprocess_image, extract_features
from signatures.models import Signature
from signatures.serializers import SignatureSerializer
from users.models import UserProfile, Address


User = get_user_model()


class SignatureVerificationIntegrationTest(TestCase):  
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
          
        # Create a test image  
        test_image = Image.new('RGB', (100, 100), color='white')  
        draw = ImageDraw.Draw(test_image)  
        draw.line((20, 50, 80, 50), fill='black', width=2)  
          
        # Convert to bytes and base64  
        buffer = BytesIO()  
        test_image.save(buffer, format='PNG')  
        image_bytes = buffer.getvalue()  
        self.base64_image = f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"  
          
        # Create test signatures with real features  
        mock_feature = np.random.rand(1, 1280) * 0.01
        for i in range(3):  
            processed_img = preprocess_image(image_bytes)  
              
            # Extract features  
            with patch('signatures.encoder.MODEL') as mock_model:  
                # Mock features for each, that are similar but not identical  
                mock_model.predict.return_value = mock_feature  
                features = extract_features(processed_img)  
              
            # Create signature  
            signature = Signature(  
                user=self.user,  
                time_ms=1000 + i * 100  
            )  
              
            # Save the file  
            file_name = f"signature_test_{i}.png"  
            signature.file.save(file_name, ContentFile(image_bytes))  
              
            # Save the features  
            signature.features = pickle.dumps(features)  
            signature.save()  
      
    @patch('signatures.encoder.extract_features')  
    def test_end_to_end_verification_success(self, mock_extract):  
        """Test end-to-end signature verification with success"""  
        # Mock extract_features to return similar features  
        stored_signature = Signature.objects.filter(user=self.user).first()  
        stored_features = pickle.loads(stored_signature.features)  
        mock_extract.return_value = stored_features  
          
        # Create a signature serializer  
        serializer = SignatureSerializer(  
            data={  
                "imgData": self.base64_image,  
                "signatureTimeMs": 1100  
            },  
            context={"request": MagicMock(user=self.user)}  
        )  
          
        # Validate and create model instance  
        self.assertTrue(serializer.is_valid())  
        signature_instance = serializer.model_instance()  
          
        # Verify the signature  
        result = self.user_profile.verify_signature(signature_instance)  
        self.assertIsNone(result)  
      
    @patch('signatures.encoder.extract_features')  
    def test_end_to_end_verification_failure(self, mock_extract):  
        """Test end-to-end signature verification with failure"""  
        # Mock extract_features to return very different features  
        mock_extract.return_value = np.random.rand(1, 1280)  
          
        # Create a signature serializer  
        serializer = SignatureSerializer(  
            data={  
                "imgData": self.base64_image,  
                "signatureTimeMs": 1100  
            },  
            context={"request": MagicMock(user=self.user)}  
        )  
          
        # Validate and create model instance  
        self.assertTrue(serializer.is_valid())  
        signature_instance = serializer.model_instance()  
          
        # Verify the signature  
        result = self.user_profile.verify_signature(signature_instance)  

        # Should fail with an error message  
        self.assertEqual(result, "Signature does not match your valid signatures.")  

    def test_create_from_instance(self):
        """Test creating a signature instance from the serializer"""
        # Create a serializer with valid data
        serializer = SignatureSerializer(
            data={
                "imgData": self.base64_image,
                "signatureTimeMs": 1100
            },
            context={"request": MagicMock(user=self.user)}
        )

        # Validate and create model instance
        self.assertTrue(serializer.is_valid())
        signature_instance = serializer.save()

        # Check that the instance has the correct attributes
        self.assertEqual(signature_instance.user, self.user)
        self.assertEqual(signature_instance.time_ms, 1100)