#from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

from django.http import HttpResponse
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
import openpyxl

#from reportlab.lib.units import inch
from openpyxl.styles import Alignment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Clases para descargar reportes:
class DescargarPDFView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="movimientos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Título
        styles = getSampleStyleSheet()
        title = Paragraph("Reporte de Movimientos Daryza", styles['Title'])
        elements.append(title)

        # Espacio después del título
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Encabezados de la tabla
        data = [["ID", "Producto", "Referencia", "Cantidad Total", "Tipo Movimiento", "Fecha Creación"]]

        # Datos de la tabla
        movimientos = Movimiento.objects.all()
        for movimiento in movimientos:
            tipo_movimiento = "Entrada" if movimiento.tipo_movimiento.descripcion == "Entrada" else "Salida"
            created_at_date = movimiento.created_at.strftime('%Y-%m-%d')
            for detalle in movimiento.detallemovimiento_set.all():
                data.append([
                    movimiento.id_movimiento,
                    detalle.producto.nombre_prod,
                    movimiento.referencia,
                    movimiento.cant_total,
                    tipo_movimiento,
                    created_at_date
                ])

        # Crear la tabla con anchos de columna ajustados
        table = Table(data, colWidths=[50, 100, 100, 100, 100, 100])  # Ajusta los anchos según sea necesario
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
            ('LEFTPADDING', (5, 0), (5, -1), 10),  # Margen izquierdo para la columna "Cantidad"
            ('RIGHTPADDING', (5, 0), (5, -1), 10),  # Margen derecho para la columna "Cantidad"
        ]))

        elements.append(table)
        doc.build(elements)
        return response


class DescargarExcelView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="movimientos.xlsx"'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Movimientos"

        # Encabezados de la tabla
        ws.append(["ID", "Referencia", "Cantidad Total", "Fecha", "Hora", "Tipo Movimiento", "Producto", "Cantidad"])

        # Datos de la tabla
        movimientos = Movimiento.objects.all()
        for movimiento in movimientos:
            tipo_movimiento = "Entrada" if movimiento.tipo_movimiento.descripcion == "Entrada" else "Salida"
            created_at_date = movimiento.created_at.strftime('%Y-%m-%d')
            created_at_time = movimiento.created_at.strftime('%H:%M:%S')
            for detalle in movimiento.detallemovimiento_set.all():
                ws.append([
                    movimiento.id_movimiento,
                    movimiento.referencia,
                    movimiento.cant_total,
                    created_at_date,
                    created_at_time,
                    tipo_movimiento,
                    detalle.producto.nombre_prod,
                    detalle.cantidad
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
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['fecha', 'tipo_movimiento']

class DetalleMovimientoViewSet(viewsets.ModelViewSet):
    queryset = DetalleMovimiento.objects.all()
    serializer_class = DetalleMovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movimiento', 'producto']

class TipoMovimientoViewSet(viewsets.ModelViewSet):
    queryset = TipoMovimiento.objects.all()
    serializer_class = TipoMovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['descripcion']



# class MovimientoViewSet(viewsets.ModelViewSet):
#     queryset = Movimiento.objects.all()
#     serializer_class = MovimientoSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['fecha', 'sucursal', 'tipo_movimiento']