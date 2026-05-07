from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_verified']
    list_filter = ['user_type', 'is_verified']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('AutoConnect', {'fields': ('user_type', 'company', 'phone', 'location', 'is_verified', 'avatar_initials', 'rating', 'review_count')}),
    )
