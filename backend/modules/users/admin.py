from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as _GroupAdmin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.models import Group as _Group

from .models import Group, User


@admin.register(Group)
class GroupAdmin(_GroupAdmin):
    pass


@admin.register(User)
class UserAdmin(_UserAdmin):
    pass


admin.site.unregister(_Group)
