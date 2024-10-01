from rest_framework.permissions import BasePermission
from .models import Perfil

class IsAlmacen(BasePermission):
    def has_permission(self, request, view):
        try:
            perfil = Perfil.objects.get(user=request.user)
            return perfil.name_role.name_role in ["Almacen", "Administrador"]
        except Perfil.DoesNotExist:
            return False

class IsVentas(BasePermission):
    def has_permission(self, request, view):
        try:
            perfil = Perfil.objects.get(user=request.user)
            return perfil.name_role.name_role in ["Ventas", "Administrador"]
        except Perfil.DoesNotExist:
            return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            perfil = Perfil.objects.get(user=request.user)
            # Solo permitir acceso a administradores
            return perfil.name_role.name_role == "Administrador"
        except Perfil.DoesNotExist:
            return False
