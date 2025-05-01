from django.test import TestCase  
from django.contrib.auth import get_user_model  
from users.models import UserProfile, Address  
  

User = get_user_model()  


class UserModelTest(TestCase):  
    def setUp(self):  
        self.address = Address.objects.create(  
            address="123 Test St",  
            city="Test City",  
            zipcode="",  
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
      
    def test_user_creation(self):  
        """Test that a user can be created with a profile"""  
        self.assertEqual(self.user.username, "testuser")  
        self.assertEqual(self.user.email, "test@example.com")  
        self.assertEqual(self.user.profile, self.user_profile)  
      
    def test_auto_fake_profile_creation(self):  
        """Test that a non-staff user gets a fake profile automatically"""  
        user = User.objects.create_user(  
            username="autoprofile",  
            email="auto@example.com",  
            password="testpassword"  
        )  
        self.assertIsNotNone(user.profile)  
        self.assertIsInstance(user.profile, UserProfile)  
      
    def test_staff_user_no_auto_profile(self):  
        """Test that staff users don't get automatic profiles"""  
        staff_user = User.objects.create_user(  
            username="staffuser",  
            email="staff@example.com",  
            password="testpassword",  
            is_staff=True  
        )  
        self.assertIsNone(staff_user.profile)


class UserProfileModelTest(TestCase):  
    def setUp(self):  
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

    def test_full_name_property(self):  
        """Test the full_name property returns the correct value"""  
        self.assertEqual(self.user_profile.full_name, "Test User")  
      
    def test_string_representation(self):  
        """Test the string representation of the UserProfile"""  
        self.assertEqual(str(self.user_profile), "Test User")
