from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name='users_in_group',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions_group',
        blank=True,
    )
