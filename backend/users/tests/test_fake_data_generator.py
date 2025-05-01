from django.test import TestCase
from users.fake_data import FakeDataGenerator  
from users.models import UserProfile, Address


class FakeDataGeneratorTest(TestCase):  
    def setUp(self):  
        self.generator = FakeDataGenerator()  
      
    def test_create_unsaved_fake_profile(self):  
        """Test that unsaved fake profiles are generated correctly"""  
        profile, address = self.generator.create_unsaved_fake_profile()  
        
        # Verify that the generated data does indeed exists.
        self.assertIsInstance(profile, UserProfile)  
        self.assertIsInstance(address, Address)  
        self.assertIsNotNone(profile.first_name)  
        self.assertIsNotNone(profile.last_name)  
        self.assertIsNotNone(profile.phone)  
        self.assertIsNotNone(profile.date_of_birth)  
        self.assertIsNotNone(profile.bank_account_number)  
          
        # Verify these aren't saved to the database yet  
        self.assertIsNone(address.id)  
        self.assertIsNone(profile.id)  
      
    def test_create_fake_profile(self):  
        """Test that fake profiles are created and saved correctly"""  
        profile = self.generator.create_fake_profile()  
          
        # Should be saved to the database.
        self.assertIsInstance(profile, UserProfile)  
        self.assertIsNotNone(profile.id)
        self.assertIsNotNone(profile.address.id)  
        self.assertIsNotNone(profile.first_name)