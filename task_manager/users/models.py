from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username
