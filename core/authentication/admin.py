from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Rol, Perfil

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


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_role')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name_role')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Perfil, ProfileAdmin)
admin.site.register(Rol, RoleAdmin)