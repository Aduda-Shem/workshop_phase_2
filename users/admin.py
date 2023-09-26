from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Define classes here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'national_id', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number'),
        }),
    )


# Register your models here.
admin.site.register(User, CustomUserAdmin)

