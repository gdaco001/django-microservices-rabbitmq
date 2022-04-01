from stocks.format_converter_strategy import FindContext, CsvToJsonConverter
from datetime import datetime

class HandleData:

    def __init__(self, data_in_csv_format):

        self.data_in_csv_format = data_in_csv_format

    def convert_and_validate_data(self):
        convert_strategy = FindContext()
        convert_strategy.setStrategy(CsvToJsonConverter())
        self.converted_data_in_json_format = convert_strategy.execute_conversion(self.data_in_csv_format)[0]
        if self.__validate_data():
            self.__convert_date_to_date_time()
            self.__filter_converted_data()
            return self.converted_data_in_json_format
        return {'detail': 'Stock not found or it does not exist.'}

    def __validate_data(self):
        if 'N/D' in self.converted_data_in_json_format.values():
            return False
        return True

    def __convert_date_to_date_time(self):
        self.converted_data_in_json_format["date"] = datetime.strptime(
            self.converted_data_in_json_format["date"] + 'T' + 
            self.converted_data_in_json_format["time"]+'Z', '%Y-%m-%dT%H:%M:%SZ')

    def __filter_converted_data(self):
        self.converted_data_in_json_format.pop('time')
        self.converted_data_in_json_format.pop('volume')
