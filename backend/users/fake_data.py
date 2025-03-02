from faker import Faker
import random
from .models import UserProfile, Address

def generate_fake_phone_number():
    """
    Generates a fake phone number in the format '+xx xxx xxxx'
    """
    country_code = f"+{random.randint(1, 99)}"
    first_part = random.randint(100, 999)
    second_part = random.randint(1000, 9999)
    return f"{country_code} {first_part} {second_part}"


# TODO: refactor as class-method for UserProfile ?
def create_fake_profile() -> UserProfile:
    """
    Generates and creates (interpret: saves to the database)
    a fake user profile and address with random data using the Faker library.
    Returns:
        UserProfile: A UserProfile object populated with fake data including
                     first name, last name, date of birth, phone number, bank
                     account number, and address details.
    """
    user_profile, address = generate_fake_data()
    address.save()
    user_profile.save()
    return user_profile
    
    
def generate_fake_data():
    """
    Generates fake user profile data using the Faker library.
    Returns:
        tuple: A tuple containing:
            - user_profile (UserProfile): An instance of UserProfile with fake data.
            - addr (Address): An instance of Address with fake data.
    """

    faker = Faker()
    first_name = faker.first_name()
    last_name = faker.last_name()
    date_of_birth = faker.date_of_birth()
    phone = faker.phone_number()
    bank_account = faker.uuid4()

    # Address
    address = faker.street_address()
    city = faker.city()
    country = faker.country_code()
    zipcode = faker.zipcode()

    addr = Address(
        address=address,
        city=city,
        country=country,
        zipcode=zipcode
    )

    user_profile = UserProfile(
        address=addr,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        date_of_birth=date_of_birth,
        bank_account_number=bank_account
    )

    return user_profile, addr
