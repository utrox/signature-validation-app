from faker import Faker
from .models import UserProfile, Address


def fake_profile() -> UserProfile:
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

    addr = Address.objects.create(
        address=address,
        city=city,
        country=country,
        zipcode=zipcode
    )

    return UserProfile.objects.create(
        address=addr,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        date_of_birth=date_of_birth,
        bank_account_number=bank_account
    )
