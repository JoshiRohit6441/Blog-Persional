from django.contrib import admin
from .models import User
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin


class CustumAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "username", "password", "verification_code"
            ),
        }),
        ("User Data", {
            "fields": (
                "first_name", "last_name", "email", "date_of_birth", "profile_photo"
            ),
        }),
        ("Contact Details", {
            "fields": (
                "Country_code_number", "phone_number"
            ),
        }),
        ("address Details", {
            "fields": (
                "address", "city", "state", "country", "zipcode"
            ),
        }),
        ("User Type", {
            "fields": (
                "is_admin", "is_active", "is_user"
            ),
        }),
        ("Groups and Permissions ", {
            "fields": (
                "groups", "user_permissions",
            ),
        }),
        ("last_login", {
            "fields": ['last_login']
        }),
    )

    list_display = ['username', "email", "first_name",
                    "last_name", "is_admin", "is_user", "is_active", "user_photo"]

    list_filter = ['is_user', 'is_active', "is_admin"]

    list_per_page = 10

    def user_photo(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.profile_photo.url)
        else:
            return 'No photo'
    user_photo.allow_tags = True
    user_photo.short_description = 'Profile Photo'


admin.site.register(User, CustumAdmin)
