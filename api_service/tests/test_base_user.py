from faker import Faker
#from api.models import User
from django.contrib.auth.models import User

from django.test import TestCase
#from django.contrib.auth.hashers import make_password

class GenerateNewRandomUserTestCase(TestCase):
    
    def setUp(self) -> None:
        faker = Faker()
        self.username = faker.user_name()
        self.password = faker.password()
        self.email = faker.email()
        self.user = User.objects.create_user(username=self.username,
                                        password=self.password,
                                        email=self.email
        )
    
    def tearDown(self) -> None:
        self.user.delete()

class GenerateNewRandomSuperUserTestCase(TestCase):
    def setUp(self) -> None:
        faker = Faker()
        self.username = faker.user_name()
        self.password = faker.password()
        self.email = faker.email()

        self.user = User.objects.create_superuser(username=self.username,
                                                  password=self.password,
                                                  email=self.email
        )


    
    def tearDown(self) -> None:
        self.user.delete()
