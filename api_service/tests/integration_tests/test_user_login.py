from tests.test_base_user import GenerateNewRandomUserTestCase
from rest_framework.test import APIClient 

class LoginTestCase(GenerateNewRandomUserTestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_should_login_with_valid_credentials(self):
        client = APIClient()
        response = client.post('/login/',
                                {
                                "username": self.username,
                                "password": self.password
                                }, format='json'
        
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue('access' in response.json())
        self.assertTrue('refresh' in response.json())

    def test_should_not_login_with_invalid_credentials(self):
        client = APIClient()
        response = client.post('/login/',
                                {
                                "username": 'some_username',
                                "password": 'some_password'
                                }, format='json'
        
        )
        self.assertNotEqual(response.status_code, 200)


    def tearDown(self) -> None:
        self.client.logout()
        return super().tearDown()

class LoginVerifyTokenTestCase(GenerateNewRandomUserTestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_should_verify_if_token_is_valid(self):
        client = APIClient()
        response = client.post('/login/',
                                {
                                "username": self.username,
                                "password": self.password
                                }, format='json'
        
        )
        verify_token_response = client.post('/verify-token/',
                                            {"token": response.json()["access"]}
        )

        self.assertEquals(verify_token_response.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        return super().tearDown()
