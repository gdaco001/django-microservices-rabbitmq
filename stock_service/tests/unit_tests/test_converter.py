from unittest import TestCase
from stocks.format_converter_strategy import FindContext, CsvToJsonConverter

class StockParserTestCase(TestCase):
    """Stock API receives data on CSV format and it must be converted to json"""

    def setUp(self) -> None:
        self.unconverted_data = 'Symbol,Date,Time,Open,High,Low,Close,Volume,Name\r\nAAPL.US,2022-03-21,21:00:06,163.51,166.35,163.015,165.38,95752860,APPLE\r\n'
        self.expected_data = {"name": str,
                             "symbol": str,
                             "open": float,
                             "high": float,
                             "low": float,
                             "close": float,
                             "volume": int,
                             "date": str,
                             "time" : str
                             }
    def test_should_convert_data_from_csv_to_json(self):
        convert_strategy = FindContext()
        convert_strategy.setStrategy(CsvToJsonConverter())
        converted_data = convert_strategy.execute_conversion(self.unconverted_data)[0]
        converted_data_dict = {key: type(value) for key, value in converted_data.items()}
        self.assertDictEqual(self.expected_data, converted_data_dict)
        