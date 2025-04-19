import logging
import random
from faker import Faker

from core.exceptions import InternalServerError
from .models import UserProfile, Address


logger = logging.getLogger(__name__)

class FakeDataGenerator: 
    def __init__(self):
        self.faker = Faker()

    def _generate_fake_phone_number(self):
        """
        Generates a fake phone number.
        
        Returns: Phone number in the format '+xx xxx xxxx'
        """
        country_code = f"+{random.randint(1, 99)}"
        first_part = random.randint(100, 999)
        second_part = random.randint(1000, 9999)
        return f"{country_code} {first_part} {second_part}"

    def _generate_fake_address(self):
        address = self.faker.street_address()
        city = self.faker.city()
        country = self.faker.country_code()
        zipcode = self.faker.zipcode()

        return Address(
            address=address,
            city=city,
            country=country,
            zipcode=zipcode
        )

    def create_unsaved_fake_profile(self):
        """
        Generates fake user profile data using the Faker library.
        Returns:
            tuple: A tuple containing:
                - user_profile (UserProfile): An instance of UserProfile with fake data.
                - addr (Address): An instance of Address with fake data.
        """
        try:
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            date_of_birth = self.faker.date_of_birth()
            phone = self._generate_fake_phone_number()
            addr = self._generate_fake_address()
            bank_account = random.randint(10000000000000000000, 999999999999999999999)

            user_profile = UserProfile(
                address=addr,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                date_of_birth=date_of_birth,
                bank_account_number=bank_account
            )

            return user_profile, addr
        except Exception as e:
            logger.exception("An error has occurred while generating fake user data: ")
            raise InternalServerError("An error has occurred while generating fake data for user profile. Please try again later. (The API might be down.)")

    def create_fake_profile(self) -> UserProfile:
        """
        Generates and creates (interpret: saves to the database)
        a fake user profile and address with random data using the Faker library.
        Returns:
            UserProfile: A UserProfile object populated with fake data including
                        first name, last name, date of birth, phone number, bank
                        account number, and address details.
        """
        user_profile, address = self.create_unsaved_fake_profile()
        address.save()
        user_profile.save()
        return user_profile
