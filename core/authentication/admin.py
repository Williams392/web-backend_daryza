from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile, ProfileType

# Register your models here.
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('id', 'first_name', 'last_name', 'email', 'phone_number')
    date_hierarchy = 'date_joined'
    ordering = ('-id',)

    fieldsets = (
        (   None, {
                "fields": ("username", "password")
            }
        ),
        (
            ("Información del usuario"), {
                'fields': ('first_name', 'last_name', 'email', 'phone_number')
            }
        ),
        (
            ("Permisos"), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
        (   ("Fechas importantes"), {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )


class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile_type')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_type')

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(ProfileType, ProfileTypeAdmin)
admin.site.register(Profile, ProfileAdmin)