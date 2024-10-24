from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create your views here.
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


# Clases para descargar reportes:
class DescargarPDFView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="movimientos.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, "Reporte de Movimientos")

        movimientos = Movimiento.objects.all()
        y = 700
        for movimiento in movimientos:
            p.drawString(100, y, f"ID: {movimiento.id_movimiento}, Referencia: {movimiento.referencia}, Cantidad Total: {movimiento.cant_total}")
            y -= 20

        p.showPage()
        p.save()
        return response

class DescargarExcelView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="movimientos.xlsx"'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Movimientos"

        ws.append(["ID", "Referencia", "Cantidad Total", "Fecha Creación"])

        movimientos = Movimiento.objects.all()
        for movimiento in movimientos:
            # Eliminar la zona horaria de created_at
            created_at = movimiento.created_at.replace(tzinfo=None)
            ws.append([movimiento.id_movimiento, movimiento.referencia, movimiento.cant_total, created_at])

        wb.save(response)
        return response



# class MovimientoViewSet(viewsets.ModelViewSet):
#     queryset = Movimiento.objects.all()
#     serializer_class = MovimientoSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['fecha', 'sucursal', 'tipo_movimiento']