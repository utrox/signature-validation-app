from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, verbose_name="user", blank=True, null=True)

    def create_fake_profile(self):
        """
        Creates a fake profile for the user if it doesn't exist.
        This is useful for non-staff users who need a profile to function.
        """
        if not self.profile:
            from .fake_data import FakeDataGenerator
            self.profile = FakeDataGenerator().create_fake_profile()
            self.save()

    def save(self, *args, **kwargs):
        if not self.profile and not self.is_staff:
            self.create_fake_profile()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=255)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    phone = models.CharField(max_length=16)
    date_of_birth = models.DateField()
    bank_account_number = models.CharField(max_length=30)

    REQUIRED_FIELDS = [
        "address", "date_of_birth", "bank_account_number"
    ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def verify_signature(self, signature_instance) -> str | None:
        """
        Verifies the validity of a given signature instance by comparing it 
        against the user's stored valid signatures.
        The verification process includes:
        1. Checking if the signature was drawn significantly slower than the 
           average time of the stored valid signatures. If it is, the signature 
           is rejected immediately to save computational resources and avoid 
           leaking information about its validity.
        2. Comparing the given signature with each stored signature using a 
           similarity metric. If the similarity score is below a predefined 
           threshold for more than one stored signature, the signature is 
           considered invalid.
        Args:
            signature_instance (Signature): The signature instance to be verified.
        Returns:
            str | None: A message indicating the failure reason of the verification. 
        """ 
        stored_signatures = self.user.signatures.all()
        
        # If the signature was drawn comparatively much slower
        # than the average of valid signatures, reject it immediately.
        # If we first check for time that means that:
        # 1.) we save computing power
        # 2.) we don't leak information about if the signature would actually be valid or not.
        signature_time_ms = signature_instance.time_ms
        avg_time = sum([sig.time_ms for sig in stored_signatures]) / len(stored_signatures)
        
        if signature_time_ms > avg_time * 2:
            print("Too slow!")
            return "Please sign your signature more dynamically."


        failures = []
        for sig in stored_signatures:
            res = sig.compare_signature(signature_instance)
            print("Comparing with: ", sig, "Result: ", res) 
            if res < settings.SIGNATURE_SIMILARITY_THRESHOLD:
                failures.append({"similarity": res, "signature": sig,})
        
        print("Failed: ", failures)
        if len(failures) > 1:
            return "Signature does not match your valid signatures."
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    zipcode = models.CharField(max_length=8)
    country = models.CharField(max_length=50)

    @property
    def formatted_address(self):
        return f"{self.address}, {self.city}, {self.zipcode}, {self.country}"

    def __str__(self):
        return self.formatted_address
