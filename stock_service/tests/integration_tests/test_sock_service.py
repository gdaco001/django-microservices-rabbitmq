from unittest import TestCase
from rest_framework.test import APIClient 
from unittest.mock import patch

class StockExternalApiGetResponseMock:
 
    def __init__(self):
        self.status_code = 200
    
    def csv(self):
        return 'Symbol,Date,Time,Open,High,Low,Close,Volume,Name\r\nAAPL.US,2022-03-21,21:00:06,163.51,166.35,163.015,165.38,95752860,APPLE\r\n'

class SockServiceTestCase(TestCase):

    def setUp(self) -> None:

        self.expected_output = {'symbol': 'AAPL.US',
                'date': '2022-03-21T21:00:06', 
                'open': 163.51, 
                'high': 166.35, 
                'low': 163.015, 
                'close': 165.38, 
                'name': 'APPLE'}

    @patch("stocks.clients.StockExternalClient.get", return_value=StockExternalApiGetResponseMock().csv())
    def test_should_retrieve_stock_info_from_external_api(self, mocked):
        self.client = APIClient()
        response = self.client.get('/stock?stock_code=aapl.us')
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(self.expected_output, response.json())

    
    def test_should_not_retrieve_stock_info_if_it_does_not_exist(self):
        self.client = APIClient()
        response = self.client.get('/stock?stock_code=some_wrong_stock_name')
        self.assertNotEquals(response.status_code, 200)
        self.assertTrue("detail" in response.json().keys())