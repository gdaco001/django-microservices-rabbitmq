from abc import ABC, abstractmethod
from api_service.settings import STOCK_SERVICE_BASE_URL
import requests
import logging

logger = logging.getLogger(__name__)

class BaseClient(ABC):

    @abstractmethod
    def get(self):
        """Interfaces client"""
        ...

class StockServiceClient(BaseClient):

    base_url = STOCK_SERVICE_BASE_URL

    def get(self, stock_code):
        """Reaches stock_service to retrieve stock info for a given stock_code"""
        stock_api_url = StockServiceClient.base_url.format(stock_code)
        response = self.__make_request('GET', stock_api_url)
        if response.status_code != 200:
            return {'detail': 'Stock not found'}
        return response.json()

    def __make_request(self, method, url, payload=None):
        try:
            logger.info(f'Trying to reach: {url}')
            return requests.request(method, url, data=payload)
        except Exception as ex:
            raise Exception(f"It was not possible to perform {method} to {url}. {str(ex)}")