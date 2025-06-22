# gestion_ventas/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from num2words import num2words 
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsVentas
from django_filters.rest_framework import DjangoFilterBackend

from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from movimientos.models import Movimiento, DetalleMovimiento, TipoMovimiento

from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsVentas
from authentication.permissions import IsAdmin


from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Comprobante
import os

from datetime import datetime, timedelta
from rest_framework.decorators import action
from django.utils.timezone import now

class ComprobantePDFView(APIView):
    
    def get(self, request, pk):
        # Buscar el comprobante por ID
        try:
            comprobante = Comprobante.objects.get(id_comprobante=pk)
        except Comprobante.DoesNotExist:
            raise Http404("Comprobante no encontrado")

        # Validar que exista el archivo PDF en `pdf_url`
        pdf_path = comprobante.pdf_url.path  # Obtener la ruta absoluta

        if not os.path.exists(pdf_path):
            raise Http404("Archivo PDF no encontrado")
        
        # Abrir y retornar el PDF como respuesta
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            return response
        
# Función para convertir el monto a letras en soles
def convertir_a_monto_letras(monto):
    enteros = int(monto)
    decimales = int(round((monto - enteros) * 100))
    
    # Convertir la parte entera del monto a palabras en español
    parte_entera_en_letras = num2words(enteros, lang='es').upper()
    # Crear la representación en letras con los céntimos
    letras = f"SON {parte_entera_en_letras} CON {decimales:02d}/100 SOLES"
    
    return letras


class ComprobanteAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk=None):
        if pk:
            try:
                comprobante = Comprobante.objects.get(id_comprobante=pk)
                serializer = ComprobanteSerializer(comprobante)
                return Response(serializer.data)
            except Comprobante.DoesNotExist:
                return Response({"error": "Comprobante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            comprobantes = Comprobante.objects.all()
            serializer = ComprobanteSerializer(comprobantes, many=True)
            return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        comprobante_data = request.data

        detalle_data = comprobante_data.pop('detalle', [])
        forma_pago_data = comprobante_data.pop('forma_pago')

        # Obtener datos del cliente
        id_cliente = comprobante_data['cliente']
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        comprobante_data['cliente'] = cliente.id_cliente

        # Obtener datos de la sucursal
        id_sucursal = comprobante_data['sucursal']
        try:
            sucursal = Sucursal.objects.get(id_sucursal=id_sucursal)
        except Sucursal.DoesNotExist:
            return Response({"error": "Sucursal no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        comprobante_data['sucursal'] = sucursal.id_sucursal

        # Asignar el usuario autenticado al comprobante
        comprobante_data['usuario'] = request.user.id_user

        # Determinar si aplica IGV según el tipo de documento
        # Boletas (tipo_doc = "03") no aplican IGV - IGV siempre 0.00
        # Facturas (tipo_doc = "01") sí aplican IGV
        aplica_igv = comprobante_data.get('tipo_doc') == "01"  # True para facturas, False para boletas

        monto_Oper_Gravadas = Decimal('0.00')
        monto_Igv = Decimal('0.00')
        sub_Total = Decimal('0.00')
        monto_Imp_Venta = Decimal('0.00')

        # Calcular valores para cada detalle
        for detalle in detalle_data:
            try:
                producto = Producto.objects.get(id_producto=detalle['id_producto'])
            except Producto.DoesNotExist:
                return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            cantidad = detalle.get('cantidad', 1)
            if producto.estock < cantidad:
                return Response({"error": "No hay suficiente stock para el producto solicitado."}, status=status.HTTP_400_BAD_REQUEST)

            producto.estock -= cantidad
            producto.save()

            tipo_movimiento_salida = TipoMovimiento.objects.get(descripcion='Salida')
            movimiento_salida = Movimiento.objects.create(
                referencia='Venta de productos',
                cant_total=cantidad,
                sucursal_id=1,
                usuario=request.user,
                tipo_movimiento=tipo_movimiento_salida,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            DetalleMovimiento.objects.create(
                cantidad=cantidad,
                producto=producto,
                movimiento=movimiento_salida
            )

            detalle['descripcion'] = producto.nombre_prod
            detalle['unidad'] = producto.unidad_medida.abreviacion
            detalle['monto_valorUnitario'] = producto.precio_venta.quantize(Decimal('0.00'))
            
            monto_valor_unitario = Decimal(detalle['monto_valorUnitario']).quantize(Decimal('0.00'))
            
            # Calcular IGV solo para facturas, para boletas siempre es 0.00
            if aplica_igv:
                igv_unitario = (monto_valor_unitario * Decimal('0.18')).quantize(Decimal('0.00'))
                detalle['monto_Precio_Unitario'] = (monto_valor_unitario + igv_unitario).quantize(Decimal('0.00'))
            else:
                igv_unitario = Decimal('0.00')
                detalle['monto_Precio_Unitario'] = monto_valor_unitario.quantize(Decimal('0.00'))

            monto_valor_venta = (monto_valor_unitario * Decimal(cantidad)).quantize(Decimal('0.00'))
            detalle['monto_Valor_Venta'] = monto_valor_venta
            
            # IGV del detalle: 0.00 para boletas, calculado para facturas
            if aplica_igv:
                igv_detalle = (monto_valor_venta * Decimal('0.18')).quantize(Decimal('0.00'))
            else:
                igv_detalle = Decimal('0.00')
            
            detalle['igv_detalle'] = igv_detalle

            monto_Oper_Gravadas += monto_valor_venta
            monto_Igv += igv_detalle
            sub_Total += (monto_valor_venta + igv_detalle)
            monto_Imp_Venta += (monto_valor_venta + igv_detalle)

        comprobante_data['detalle'] = detalle_data
        comprobante_data['forma_pago'] = forma_pago_data
        comprobante_data['monto_Oper_Gravadas'] = monto_Oper_Gravadas.quantize(Decimal('0.00'))
        comprobante_data['monto_Igv'] = monto_Igv.quantize(Decimal('0.00'))  # Será 0.00 para boletas
        comprobante_data['valor_venta'] = monto_Oper_Gravadas.quantize(Decimal('0.00'))
        comprobante_data['sub_Total'] = sub_Total.quantize(Decimal('0.00'))
        comprobante_data['monto_Imp_Venta'] = monto_Imp_Venta.quantize(Decimal('0.00'))

        forma_pago_data['monto'] = monto_Imp_Venta.quantize(Decimal('0.00'))
        comprobante_data['forma_pago'] = forma_pago_data

        legend_value = convertir_a_monto_letras(monto_Imp_Venta)
        comprobante_data['legend_comprobante'] = {
            "legend_code": "1000",
            "legend_value": legend_value
        }

        # Crear el comprobante
        comprobante_serializer = ComprobanteSerializer(data=comprobante_data)
        if comprobante_serializer.is_valid():
            comprobante = comprobante_serializer.save()
            cliente_num_doc = cliente.ruc_cliente if comprobante.tipo_doc == "01" or comprobante.cliente_tipo_doc == "6" else cliente.dni_cliente

            response_data = comprobante_serializer.data
            response_data['cliente'] = {
                'id_cliente': cliente.id_cliente,
                'cliente_num_doc': cliente_num_doc,
                'cliente_denominacion': f"{cliente.nombre_clie} {cliente.apellido_clie}" if comprobante.cliente_tipo_doc == "1" else cliente.razon_socialCliente,
                'cliente_direccion': cliente.direccion_clie
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(comprobante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        comprobante = get_object_or_404(Comprobante, pk=pk)
        serializer = ComprobanteSerializer(comprobante, data=request.data, partial=True)
        if serializer.is_valid():
            comprobante = serializer.save()
            return Response(ComprobanteSerializer(comprobante).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comprobante = get_object_or_404(Comprobante, id_comprobante=pk)
        comprobante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_sucursal']

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_clie', 'dni_cliente', 'ruc_cliente']


class FormaPagoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'monto']

class LegendViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Legend.objects.all()
    serializer_class = LegendSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['legend_code', 'comprobante']
