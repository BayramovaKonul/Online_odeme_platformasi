from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel, UserGroupModel

class CustomUserAdmin(UserAdmin):
    model = CustomUserModel

    list_display = ("phone_number", "name", "surname", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Information", {"fields": ("name", "surname")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "name", "surname", "password1", "password2", "is_staff"),
        }),
    )

    search_fields = ("phone_number", "name", "surname")
    ordering = ("phone_number",)


# Register the CustomUser model with the customized admin
admin.site.register(CustomUserModel, CustomUserAdmin)


@admin.register(UserGroupModel)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name'] 
    filter_horizontal = ('groups',)

  
