from django.contrib import admin
from .models import CustomUser, Department, Profile
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location','description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['name', 'description']


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birthday','photo']
    raw_id_fields = ['user']