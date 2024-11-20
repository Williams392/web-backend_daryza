# reports/dashboard.py
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from django.utils.timezone import now
from rest_framework import viewsets

from django.db.models import F, Sum

from gestion_venta.models import Comprobante
from gestion_venta.models import Cliente
from authentication.models import CustomUser
from gestion_almacen.models import Producto 
from movimientos.models import Movimiento, TipoMovimiento

from django.db.models.functions import TruncDate, TruncMonth

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


class DashboardViewComprobanteSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def conteo_y_aumento_comprobantes(self, request):
        total_comprobantes = Comprobante.objects.count()

        # Obtener comprobantes creados en el último mes
        fecha_hace_un_mes = now() - timedelta(days=30)
        comprobantes_mes_anterior = Comprobante.objects.filter(fecha_emision__lt=fecha_hace_un_mes).count()

        # Calcular el porcentaje de aumento
        if comprobantes_mes_anterior == 0:
            porcentaje_aumento_comprobantes = 100  # Suponemos un aumento del 100% si no había comprobantes antes
        else:
            porcentaje_aumento_comprobantes = ((total_comprobantes - comprobantes_mes_anterior) / comprobantes_mes_anterior) * 100

        return Response({
            "total_comprobantes": total_comprobantes,
            "porcentaje_aumento_comprobantes": porcentaje_aumento_comprobantes
        })
    
    # GRAFICO:
    @action(detail=False, methods=['get'])
    def ventas_por_dia_semana(self, request):
        fecha_actual = now()
        fecha_inicio = fecha_actual - timedelta(days=7)
        
        ventas_diarias = Comprobante.objects.filter(fecha_emision__gte=fecha_inicio).extra(
            select={'dia_semana': "DATEPART(weekday, fecha_emision)"}
        ).values('dia_semana').annotate(total_ventas=Sum('monto_Imp_Venta')).order_by('dia_semana')
        
        dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        ventas_diarias = [{**venta, 'dia_semana': dias_semana[int(venta['dia_semana']) - 1]} for venta in ventas_diarias]
        
        return Response(ventas_diarias)
    
from django.db.models.functions import TruncDay
class DashboardVieMovieminentoSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def movimientos_semanales(self, request):
        """
        Obtiene los movimientos de entrada y salida de la última semana
        agrupados por día de la semana.
        """
        try:
            fecha_inicio = now() - timedelta(days=7)
            movimientos = (
                Movimiento.objects.filter(created_at__gte=fecha_inicio)
                .annotate(
                    tipo=F('tipo_movimiento__descripcion'),
                    dia_semana=TruncDay('created_at')  # Para obtener solo la fecha (sin hora)
                )
                .values('tipo', 'dia_semana')
                .annotate(total_cantidad=Sum('cant_total'))
                .order_by('dia_semana')
            )

            # Mapeamos los números de los días a los nombres en español
            dias_semana = {
                0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 
                4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
            }

            # Formatear la respuesta para el gráfico
            respuesta = {}
            for movimiento in movimientos:
                dia_num = movimiento['dia_semana'].weekday()  # Obtiene el número del día de la semana (0=Monday, 6=Sunday)
                dia = dias_semana[dia_num]
                tipo = movimiento['tipo']
                if dia not in respuesta:
                    respuesta[dia] = {'Entradas': 0, 'Salidas': 0}
                if tipo == 'Entrada':
                    respuesta[dia]['Entradas'] += movimiento['total_cantidad']
                elif tipo == 'Salida':
                    respuesta[dia]['Salidas'] += movimiento['total_cantidad']

            # Ordenar por día de la semana y convertir a lista para Angular
            grafico_data = [
                {'dia_semana': dia, 'entradas': data['Entradas'], 'salidas': data['Salidas']}
                for dia, data in respuesta.items()
            ]

            # Retornar los datos formateados
            return Response(grafico_data)

        except Exception as e:
            # Capturar cualquier error inesperado
            return Response({'error': str(e)}, status=500)

