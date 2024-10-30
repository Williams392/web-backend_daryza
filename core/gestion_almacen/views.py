from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Marca, UnidadMedida, Producto
from .serializers import CategoriaSerializer, MarcaSerializer, UnidadMedidaSerializer, ProductoSerializer

from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAlmacen
from movimientos.models import Movimiento, DetalleMovimiento, TipoMovimiento
from django.db import transaction
from django.utils import timezone
import uuid 

from django.http import HttpResponse
import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl

# REPORTE DE PRODUCTOS:
class DescargarPDFView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Título
        styles = getSampleStyleSheet()
        title = Paragraph("Reporte de Productos Daryza", styles['Title'])
        elements.append(title)

        # Espacio después del título
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Encabezados de la tabla
        data = [["ID", "Nombre", "Precio Compra", "Precio Venta", "Estado", "Stock", "Creado", "Marca"]]

        # Datos de la tabla
        productos = Producto.objects.all()
        for producto in productos:
            data.append([
                producto.id_producto,
                producto.nombre_prod,
                producto.precio_compra,
                producto.precio_venta,
                "Activo" if producto.estado else "Inactivo",
                producto.estock,
                producto.created_at.strftime('%Y-%m-%d'),
                producto.marca.nombre_marca  # Asegúrate de que `marca` tiene un campo `nombre`
            ])

        # Crear la tabla con anchos de columna ajustados
        table = Table(data, colWidths=[30, 100, 100, 80, 50, 50, 80, 80])  # Ajustar el ancho de "Precio Compra"
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

class DescargarExcelView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Productos"

        # Encabezados de la tabla
        ws.append(["ID", "Nombre", "Precio Compra", "Precio Venta", "Estado", "Stock", "Creado", "Marca"])

        # Datos de la tabla
        productos = Producto.objects.all()
        for producto in productos:
            ws.append([
                producto.id_producto,
                producto.nombre_prod,
                producto.precio_compra,
                producto.precio_venta,
                "Activo" if producto.estado else "Inactivo",
                producto.estock,
                #producto.estock_minimo,
                producto.created_at.strftime('%Y-%m-%d'),
                producto.marca.nombre_marca  
            ])

        # Ajustar el ancho de las columnas
        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        wb.save(response)
        return response
    

# CRUD:
class ProductoFilter(filters.FilterSet):
    nombre_prod = filters.CharFilter(lookup_expr='icontains') 
    marca = filters.CharFilter(field_name='marca__nombre', lookup_expr='icontains')  
    categoria = filters.CharFilter(field_name='categoria__nombre', lookup_expr='icontains') 

    class Meta:
        model = Producto
        fields = ['nombre_prod', 'codigo', 'marca', 'categoria']

class ProductoView(APIView):
    # permission_classes = [IsAuthenticated, IsAlmacen]
    # quite el permiso para el user ventas puede aceder a producto.
    
    def get(self, request, pk_producto=None):
        if pk_producto:  # Ver detalles de un producto específico
            producto = get_object_or_404(Producto, pk=pk_producto)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data)
        else:  # Ver todos los productos
            queryset = Producto.objects.all()
            # Aplica filtros manualmente
            filtro = ProductoFilter(request.GET, queryset=queryset)
            productos = filtro.qs  # Obtiene los productos filtrados
            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()

            # Crear el movimiento de entrada
            tipo_movimiento = TipoMovimiento.objects.get(descripcion='Entrada')
            movimiento = Movimiento.objects.create(
                referencia='Ingreso de productos',
                cant_total=producto.estock,
                sucursal_id=1,  # Sucursal, puedes cambiar esto según tu lógica
                usuario=request.user,  # Usuario que crea el producto
                tipo_movimiento=tipo_movimiento,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            # Crear el detalle del movimiento
            DetalleMovimiento.objects.create(
                cantidad=producto.estock,
                producto=producto,
                movimiento=movimiento
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def put(self, request, pk_producto=None):
        producto = get_object_or_404(Producto, pk=pk_producto)
        serializer = ProductoSerializer(producto, data=request.data, partial=True)  # partial=True permite actualización parcial

        if serializer.is_valid():
            serializer.save()  # La lógica de actualización de la imagen ya está manejada en el serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_producto=None):
        producto = get_object_or_404(Producto, pk=pk_producto)
        producto.delete()
        return Response({"msg": f"Producto con ID {pk_producto} ha sido eliminado"})
    

class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAlmacen]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_categoria', 'estado_categoria']

class MarcaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAlmacen]
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_marca', 'estado_marca']

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAlmacen]
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_unidad', 'abreviacion']