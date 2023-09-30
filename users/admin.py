# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'national_id', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number'),
        }),
    )

    def register_user(self, request, queryset):
        for user in queryset:
            user.is_active = True  
            user.save()

        self.message_user(request, 'Selected users have been registered successfully.')

    register_user.short_description = 'Register selected users'

admin.site.register(User, CustomUserAdmin)
