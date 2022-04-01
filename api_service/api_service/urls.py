# encoding: utf-8

from django.contrib import admin
from django.urls import path

from api import views as api_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("stock", api_views.StockView.as_view(), name="stock_retrieve"),
    path("history", api_views.HistoryView.as_view(), name="history_list"),
    path("stats", api_views.StatsView.as_view(), name="stats_retrieve"),
    path("admin", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-token/", TokenVerifyView.as_view(), name="token_verify"),
]
