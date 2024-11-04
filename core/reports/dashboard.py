# reports/dashboard.py
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import viewsets


from gestion_venta.models import Cliente
class DashboardViewClienteSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def conteo_y_aumento_clientes(self, request):
        total_clientes = Cliente.objects.count()
        
        # Obtener clientes creados en el último mes
        fecha_hace_un_mes = now() - timedelta(days=30)
        clientes_mes_anterior = Cliente.objects.filter(fecha_creacion__lt=fecha_hace_un_mes).count()
        
        # Calcular el porcentaje de aumento
        if clientes_mes_anterior == 0:
            porcentaje_aumento_clientes = 100  # Suponemos un aumento del 100% si no había clientes antes
        else:
            porcentaje_aumento_clientes = ((total_clientes - clientes_mes_anterior) / clientes_mes_anterior) * 100

        return Response({
            "total_clientes": total_clientes,
            "porcentaje_aumento_clientes": porcentaje_aumento_clientes
        })


from gestion_almacen.models import Producto 
class DashboardViewProductoSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def conteo_y_aumento_productos(self, request):
        total_productos = Producto.objects.count()
        
        # Obtener productos creados en el último mes
        fecha_hace_un_mes = now() - timedelta(days=30)
        productos_mes_anterior = Producto.objects.filter(created_at__lt=fecha_hace_un_mes).count()
        
        # Calcular el porcentaje de aumento
        if productos_mes_anterior == 0:
            porcentaje_aumento_producto = 100  # Suponemos un aumento del 100% si no había productos antes
        else:
            porcentaje_aumento_producto = ((total_productos - productos_mes_anterior) / productos_mes_anterior) * 100

        return Response({
            "total_productos": total_productos,
            "porcentaje_aumento_producto": porcentaje_aumento_producto
        })
    
from authentication.models import CustomUser
class DashboardViewUsuarioSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def conteo_y_aumento_usuarios(self, request):
        total_usuarios = CustomUser.objects.count()

        # Obtener usuarios creados en el último mes
        fecha_hace_un_mes = now() - timedelta(days=30)
        usuarios_mes_anterior = CustomUser.objects.filter(date_joined__lt=fecha_hace_un_mes).count()

        # Calcular el porcentaje de aumento
        if usuarios_mes_anterior == 0:
            porcentaje_aumento_usuarios = 100  # Suponemos un aumento del 100% si no había usuarios antes
        else:
            porcentaje_aumento_usuarios = ((total_usuarios - usuarios_mes_anterior) / usuarios_mes_anterior) * 100

        return Response({
            "total_usuarios": total_usuarios,
            "porcentaje_aumento_usuarios": porcentaje_aumento_usuarios
        })