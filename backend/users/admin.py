from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('email', 'last_name', 'first_name', 'second_name', 'role')
