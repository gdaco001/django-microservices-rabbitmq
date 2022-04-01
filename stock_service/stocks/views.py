# encoding: utf-8

from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny

from django.http import JsonResponse

from stocks.clients import StockExternalClient
from stocks.utils import HandleData


class StockView(mixins.RetrieveModelMixin, generics.GenericAPIView):

    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        client = StockExternalClient()
        stock_code = request.query_params.get("stock_code")
        csv_data = client.get(stock_code)
        data_handler = HandleData(csv_data)
        data = data_handler.convert_and_validate_data()
        if "detail" in data.keys():
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        print(data)
        return JsonResponse(data)
