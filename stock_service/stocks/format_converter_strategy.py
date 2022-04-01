import pandas as pd
import io
import json

from abc import ABC, abstractmethod


class ConverterStrategy(ABC):
    """Extend for further conversion methods"""
    @abstractmethod
    def convert(self):
        """Converts from one format to another"""
        ...

class JsonToCsvConverter(ConverterStrategy):
    ...


class CsvToJsonConverter(ConverterStrategy):

    def convert(self, data):
        read_csv_data = pd.read_csv(io.StringIO(data), sep = ",")
        csv_data = pd.DataFrame(read_csv_data)
        csv_data.columns= csv_data.columns.str.lower()
        json_string_data = csv_data.to_json(orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
        json_data = json.loads(json_string_data)
        return json_data

class FindContext:
    strategy: ConverterStrategy

    def setStrategy(self, strategy: ConverterStrategy):
        self.strategy = strategy

    def execute_conversion(self, data):
        return self.strategy.convert(data)
