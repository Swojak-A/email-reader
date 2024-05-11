from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as _Group


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"


class Group(_Group):
    class Meta:
        proxy = True
