import logging

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationViewsTestsBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_password = 'StrongP@ssw0rd'
        self.user = User.objects.create_user(username='testuser', password=self.user_password)
        logging.disable(logging.CRITICAL)
