# permissions.py

from rest_framework.permissions import BasePermission
from .models import Rol

class IsAlmacen(BasePermission):
    def has_permission(self, request, view):
        # Verificar si el usuario tiene un rol
        if request.user.is_authenticated:
            return request.user.name_role.name_role in ["Almacen", "Administrador"]
        return False

class IsVentas(BasePermission):
    def has_permission(self, request, view):
        # Verificar si el usuario tiene un rol
        if request.user.is_authenticated:
            return request.user.name_role.name_role in ["Ventas", "Administrador"]
        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Verificar si el usuario tiene un rol
        if request.user.is_authenticated:
            return request.user.name_role.name_role == "Administrador"
        return False
