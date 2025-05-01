import unittest  
import numpy as np  
from PIL import ImageDraw  

from io import BytesIO  
from unittest.mock import patch, MagicMock  
from PIL import Image  

from django.conf import settings  
from signatures.encoder import preprocess_image, extract_features, compare_features  
  

class EncoderTest(unittest.TestCase):  
    def setUp(self):  
        # Create a simple test image  
        self.test_image = Image.new('RGB', (100, 100), color='white')  
        draw = ImageDraw.Draw(self.test_image)  
        draw.line((20, 50, 80, 50), fill='black', width=2)  
        draw.line((50, 20, 50, 80), fill='black', width=2)  
          
        # Convert to bytes  
        buffer = BytesIO()  
        self.test_image.save(buffer, format='PNG')  
        self.image_bytes = buffer.getvalue()  
          
        # Create test feature vectors -
        # features1 & features2 are almost identical. features3 is very different  
        self.features1 = np.array([[0.1, 0.2, 0.3, 0.4]])  
        self.features2 = np.array([[0.1, 0.25, 0.3, 0.4]])  
        self.features3 = np.array([[1.0, 0.0, 0.05, 1.0]])  

    def _test_processing_bytes(self, image_bytes):
        """Test preprocessing an image from bytes"""  
        # Process the image  
        processed = preprocess_image(image_bytes)  
          
        # Check the shape and type  
        self.assertEqual(processed.shape, (1, 224, 224, 3))  
        self.assertEqual(processed.dtype, np.float32)  
    
    def test_preprocess_image_rgb(self):  
        """Test preprocessing an RGB image"""  
        self._test_processing_bytes(self.image_bytes)
      
    def test_preprocess_image_rgba(self):  
        """Test preprocessing an RGBA image"""
        # Convert test image to RGBA
        rgba_image = self.test_image.convert('RGBA')
        buffer = BytesIO()
        rgba_image.save(buffer, format='PNG')
        rgba_bytes = buffer.getvalue()
        
        self._test_processing_bytes(rgba_bytes)
      
    def test_preprocess_image_grayscale(self):  
        """Test preprocessing a grayscale image"""  
        # Convert test image to grayscale  
        gray_image = self.test_image.convert('L')  
        buffer = BytesIO()  
        gray_image.save(buffer, format='PNG')  
        gray_bytes = buffer.getvalue()  
          
        # Process the image 
        self._test_processing_bytes(gray_bytes) 
      
    @patch('signatures.encoder.MODEL')  
    def test_extract_features__called(self, mock_model):  
        """Test feature extraction calls MODEL's predict method correctly"""  
        # Mock the model's predict method  
        mock_features = np.random.rand(1, 1280)  
        mock_model.predict.return_value = mock_features  
          
        # Create a test preprocessed image and extract it's features
        test_img = np.random.rand(1, 224, 224, 3)  
        features = extract_features(test_img)  
          
        # Check that the model was called with the test image and the mocked features were returned 
        mock_model.predict.assert_called_once_with(test_img)  
        np.testing.assert_array_equal(features, mock_features)  
      
    def test_compare_features_identical__almost_1_0(self):  
        """Test comparing identical feature vectors"""  
        # Compare identical features  
        similarity = compare_features(self.features1, self.features2)  
          
        # Should be over the threshold, as they are very similar
        self.assertGreaterEqual(similarity[0][0], settings.SIGNATURE_SIMILARITY_THRESHOLD)  
      
    def test_compare_features_different__less_than_1_0(self):  
        """Test comparing different feature vectors"""  
        # Compare different features  
        similarity = compare_features(self.features1, self.features3)  
          
        # Should be less than the threshold, as they are very different.
        self.assertLess(similarity[0][0], settings.SIGNATURE_SIMILARITY_THRESHOLD)  
      
    def test_compare_features_invalid_shape__value_error(self):
        """Test comparing features with invalid shapes"""
        # Create features with different shapes
        vec1 = np.array([[1.0, 0.0]])
        vec2 = np.array([[0.0, 1.0, 0.0]])
        
        # Compare features
        with self.assertRaises(ValueError):
            compare_features(vec1, vec2)
