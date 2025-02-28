from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, verbose_name="user", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.profile and not self.is_staff:
            raise ValidationError("Non-staff user cannot exist without Profile data.")
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


class Address(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=60)
    zipcode = models.CharField(max_length=8)
    country = models.CharField(max_length=50)

    def get_formatted_address(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}, {self.country}"

    def __str__(self):
        return self.get_formatted_address()
