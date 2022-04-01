from abc import ABC, abstractmethod
from stock_service.settings import STOCK_SERVICE_EXTERNAL_API_URL
import requests


class BaseClient(ABC):

    @abstractmethod
    def get(self):
        """Interfaces client"""
        ...

class StockExternalClient(BaseClient):

    api_url = STOCK_SERVICE_EXTERNAL_API_URL

    def get(self, stock_code):
        stock_api_url = StockExternalClient.api_url.format(stock_code)
        response = self.__make_request('GET', stock_api_url)
        data_in_csv_format = response.text
        return data_in_csv_format

    def __make_request(self, method, url, payload=None):
        return requests.request(method, url, data=payload)
