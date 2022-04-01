# encoding: utf-8

from rest_framework import serializers
from datetime import datetime

from api.models import UserRequestHistory

from django.contrib.auth.models import User


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context["request"]
        if hasattr(request, "user") and request.user:
            return request.user
        return None

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class UserRequestHistorySerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=CurrentUserDefault())

    def to_internal_value(self, data):

        data["open"] = round(data["open"], 2)
        data["high"] = round(data["high"], 2)
        data["low"] = round(data["low"], 2)
        data["close"] = round(data["close"], 2)

        return super().to_internal_value(data)

    class Meta:
        model = UserRequestHistory
        exclude = ["id"]
