# enconding: utf-8

from django.conf import settings
from djongo import models

from datetime import datetime, timedelta

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

# class UserManager(BaseUserManager):
#     """
#     Define Manager for custom User model
#     """

#     def create_user(self, username, email, password=None,**extra_fields):
#         """Create and return a `User` with an email, username and password."""
#         if username is None:
#             raise TypeError('Users must have a username.')

#         if email is None:
#             raise TypeError('Users must have an email address.')

#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()

#         return user

#     def create_superuser(self, username, email, password, **extra_fields):
#         """
#         Create and return a `User` with superuser (admin) permissions.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

#         return user

# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = UserManager()

#     def __str__(self):
#         """
#         String representation of `User`.
#         """
#         return self.email

#     def get_full_name(self):
#         """
#         Since we are not storing real names, return username.
#         """
#         return self.username

#     def get_short_name(self):
#         """
#         Since we are not storing real names, return username.
#         """
#         return self.username

class UserRequestHistory(models.Model):
    """
    Model to store the requests done by each user.
    """
    date = models.DateTimeField()
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
