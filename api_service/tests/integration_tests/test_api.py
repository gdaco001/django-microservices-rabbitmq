from tests.test_base_user import (
    GenerateNewRandomUserTestCase,
    GenerateNewRandomSuperUserTestCase,
)
from tests.test_database_data import GenerateDatabaseEntriesTestCase
from rest_framework.test import APIClient
from api.models import UserRequestHistory
from .mocks import (
    StatsApiGetResponseMock,
    HistoryApiGetResponseMock,
    StockApiGetResponseMock,
)

from django.urls import reverse
from unittest.mock import patch


class UserPermissionsTestCase(GenerateNewRandomUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        response = self.client.post(
            "/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.access_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.invalid_access_token = "eyJ0eX4234JKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ3ODQzNjQ1LCJpYXQiOjE2NDc4NDMzNDUsImp0aSI6IjdjNzU3Zjc1MzU1ZjRjNTg4NWQ0N2UzZjNjNjQzABCyIiwidXNlcl9pZCI6MTR9.KZKmKUtyTfs-5YdZf4eVZbI3RCoF61IscGCvE3GMu72"

    def test_should_not_allow_access_to_unauthenticated_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.invalid_access_token
        )
        response = self.client.get("/stats")
        self.assertEquals(response.status_code, 401)
        response = self.client.get("/stock")
        self.assertEquals(response.status_code, 401)
        response = self.client.get("/history")
        self.assertEquals(response.status_code, 401)

    def test_should_not_allow_access_to_stats_endpoint_for_authenticated_regular_users(
        self,
    ):
        response = self.client.get("/stats")
        self.assertEquals(response.status_code, 403)


class StockEndpointTestCase(GenerateNewRandomUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        response = self.client.post(
            "/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.access_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.url = reverse("stock_retrieve")

    @patch(
        "api.clients.StockServiceClient.get",
        return_value=StockApiGetResponseMock().json(),
    )
    def test_should_retrieve_stock_info_and_save_on_database(self, mocked):
        response = self.client.get(self.url + "?q=aapl.us", format="json")
        self.assertEquals(response.status_code, 200)
        histories = UserRequestHistory.objects.all()
        self.assertEquals(len(histories), 1)
        saved_history = histories.first()
        self.assertEquals(saved_history.symbol, "GAPL.US")

    def test_should_not_retrieve_stock_info_if_it_does_not_exist_or_is_not_found(self):
        response = self.client.get(self.url + "?q=some_wrong_stock_code", format="json")
        self.assertEquals(response.status_code, 404)
        response = self.client.get(self.url + "?q=", format="json")
        self.assertEquals(response.status_code, 404)
        response = self.client.get(self.url, format="json")
        self.assertEquals(response.status_code, 404)

    def tearDown(self) -> None:
        self.client.logout()
        return super().tearDown()


class HistoryEndpointTestCase(GenerateDatabaseEntriesTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        response = self.client.post(
            "/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.access_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.stats_url = reverse("history_list")

    def test_should_list_history_of_queries_made_by_user(self):
        response = self.client.get(self.stats_url)
        self.assertEquals(HistoryApiGetResponseMock().json(), response.json())

    def tearDown(self) -> None:
        self.client.logout()
        return super().tearDown()


class StatsEndpointTestCase(GenerateDatabaseEntriesTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        response = self.client.post(
            "/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.access_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.invalid_access_token = "eyJ0eX4234JKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ3ODQzNjQ1LCJpYXQiOjE2NDc4NDMzNDUsImp0aSI6IjdjNzU3Zjc1MzU1ZjRjNTg4NWQ0N2UzZjNjNjQzABCyIiwidXNlcl9pZCI6MTR9.KZKmKUtyTfs-5YdZf4eVZbI3RCoF61IscGCvE3GMu72"
        self.stats_url = reverse("stats_retrieve")

    def test_should_return_top_5_most_requested_stocks(self):
        response = self.client.get(self.stats_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 5)
        self.assertListEqual(StatsApiGetResponseMock().json(), response.json())

    def test_should_not_allow_access_to_unauthenticated_superuser(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.invalid_access_token
        )
        response = self.client.get("/stats")
        self.assertEquals(response.status_code, 401)

    def tearDown(self) -> None:
        self.client.logout()
        return super().tearDown()
