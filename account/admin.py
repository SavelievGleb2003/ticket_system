from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("department",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("department",)}),
    )
    list_display = ("username", "email", "first_name", "last_name", "department", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "department__name")
    list_filter = ("department", "is_staff", "is_active")