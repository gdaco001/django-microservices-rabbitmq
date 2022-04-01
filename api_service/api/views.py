# encoding: utf-8

from logging import raiseExceptions
from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.http import JsonResponse
from django.db.models import Count

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer

from api.clients import StockServiceClient

from .utils import replace_symbol_key_to_stock


class StockView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Endpoint to allow users to query stocks
    When a user makes a request to get a stock quote (calls the stock endpoint in the api service),
    if a stock is found, it should be saved in the database associated to the user making the request.
    """

    serializer_class = UserRequestHistorySerializer

    def get(self, request, *args, **kwargs):

        client = StockServiceClient()
        stock_code = request.query_params.get("q")
        data = client.get(stock_code)
        if "detail" in data:
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data)


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """

    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer

    def get(self, request, *args, **kwargs):
        filter = self.queryset.filter(user=request.user.id).order_by("-id")
        serializer = self.get_serializer(filter, many=True)
        return Response(serializer.data)


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """

    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        q = (
            UserRequestHistory.objects.values("symbol")
            .annotate(times_requested=Count("symbol"))
            .order_by("-times_requested")[:5]
        )
        q = list(q)
        q = map(replace_symbol_key_to_stock, q)
        return Response(q)
