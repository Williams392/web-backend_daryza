# Reporte PDF Y EXCEL - PRODUCTOS:

from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Producto

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