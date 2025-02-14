from django.contrib import admin
from .models import CustomUser, Department, Profile, Position
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location','description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['name', 'description']


@admin.register(Position)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'department','description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description']
    ordering = ['title', 'description']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # Check if it's a new user
        super().save_model(request, obj, form, change)
        if is_new:
            Profile.objects.create(user=obj)

    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("department",)}),
        ("Additional Info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("department",)}),
        ("Additional Info", {"fields": ("position",)}),
    )
    list_display = ("username", "email", "first_name", "last_name",'position', "department", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name","position__name", "department__name")
    list_filter = ("department", "is_staff", "is_active")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birthday','photo']
    raw_id_fields = ['user']