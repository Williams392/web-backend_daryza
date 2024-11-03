# dashboard.py
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import viewsets


from gestion_venta.models import Cliente  # Ajusta la importación según tu estructura de carpetas
class DashboardViewClienteSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def conteo_y_aumento_clientes(self, request):
        total_clientes = Cliente.objects.count()
        
        # Obtener clientes creados en el último mes
        fecha_hace_un_mes = now() - timedelta(days=30)
        clientes_mes_anterior = Cliente.objects.filter(fecha_creacion__lt=fecha_hace_un_mes).count()
        
        # Calcular el porcentaje de aumento
        if clientes_mes_anterior == 0:
            porcentaje_aumento = 100  # Suponemos un aumento del 100% si no había clientes antes
        else:
            porcentaje_aumento = ((total_clientes - clientes_mes_anterior) / clientes_mes_anterior) * 100

        return Response({
            "total_clientes": total_clientes,
            "porcentaje_aumento": porcentaje_aumento
        })


from gestion_almacen.models import Producto  # falta
class DashboardViewProductoSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def conteo_y_aumento_productos(self, request):
        total_productos = Producto.objects.count()
        
        # Obtener productos creados en el último mes
        fecha_hace_un_mes = now() - timedelta(days=30)
        productos_mes_anterior = Producto.objects.filter(fecha_creacion__lt=fecha_hace_un_mes).count()
        
        # Calcular el porcentaje de aumento
        if productos_mes_anterior == 0:
            porcentaje_aumento = 100  # Suponemos un aumento del 100% si no había productos antes
        else:
            porcentaje_aumento = ((total_productos - productos_mes_anterior) / productos_mes_anterior) * 100

        return Response({
            "total_productos": total_productos,
            "porcentaje_aumento": porcentaje_aumento
        })