# Reporte PDF Y EXCEL - PRODUCTOS:

from django.http import HttpResponse
from rest_framework.views import APIView
from gestion_almacen.models import Producto

import csv
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os
import openpyxl
from datetime import datetime


# REPORTE DE PRODUCTOS:
class DescargarPDFproductoView(APIView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        
        # Crear el encabezado como una función
        def draw_header(canvas, doc):
            width, height = A4

            # Encabezado ajustado para reducir la altura
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.setLineWidth(1)
            canvas.rect(30, height - 98, width - 60, 70)  # Reducir la altura del rectángulo

            # Dividir el encabezado en tres columnas
            col_width = (width - 60) / 3

            # Ajustar coordenada vertical (y) para alinear los elementos
            y_position = height - 70  # Posición inicial del logo

            # Logo
            logo_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'logo-daryza_v2.png')
            logo_width = 200  # Ajusta el ancho como necesites
            logo_height = 47  # Aumentar la altura del logo
            # Ajustar la posición y para mantener el logo dentro del marco
            canvas.drawImage(logo_path, 31, y_position - (logo_height - 33), width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

            # Datos de la empresa (centrados y alineados con el logo)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawCentredString(30 + col_width + col_width / 2, y_position + 20, "Daryza S.A.C.")
            canvas.setFont("Helvetica", 9)
            canvas.drawCentredString(30 + col_width + col_width / 2, y_position + 5, "Dirección: Lurin, Lima, Lima")
            canvas.drawCentredString(30 + col_width + col_width / 2, y_position - 10, "Email: daryza@gmail.com")

            # Título del reporte
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawCentredString(30 + 2 * col_width + col_width / 2, y_position + 20, "REPORTE")

            # Fecha y hora (alineada con el logo y los datos de la empresa)
            canvas.setFont("Helvetica", 9)
            fecha = datetime.now().strftime("%d/%m/%Y")
            hora = datetime.now().strftime("%H:%M:%S")
            canvas.drawCentredString(30 + 2 * col_width + col_width / 2, y_position + 5, f"Fecha: {fecha}")
            canvas.drawCentredString(30 + 2 * col_width + col_width / 2, y_position - 10, f"Hora: {hora}")

        # Título más cerca del encabezado
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontSize = 16
        title_style.leading = 15
        title = Paragraph("REPORTE DE PRODUCTOS DARYZA", title_style)

        # Reducir el espaciado para acercar el título al encabezado
        elements.append(Spacer(1, 35))
        elements.append(title)
        elements.append(Spacer(1, 15))

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
                producto.marca.nombre_marca
            ])

        # Definir anchos de columnas ajustados
        table = Table(data, colWidths=[
            (A4[0] - 60) * 0.08,  # ID un 20 % más pequeño (ajuste aproximado)
            (A4[0] - 60) * 0.18,  # Nombre
            (A4[0] - 60) * 0.16,  # Precio Compra (más ancho)
            (A4[0] - 60) * 0.12,  # Precio Venta
            (A4[0] - 60) * 0.12,  # Estado
            (A4[0] - 60) * 0.1,   # Stock
            (A4[0] - 60) * 0.12,  # Creado
            (A4[0] - 60) * 0.12   # Marca
        ])

        # Estilo de la tabla
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        doc.build(elements, onFirstPage=draw_header, onLaterPages=draw_header)
        return response


class DescargarExcelProductoView(APIView):
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
    
    