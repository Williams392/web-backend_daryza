from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from django.conf import settings
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from decimal import Decimal
import os

def generar_pdf_comprobante(comprobante_data):

    # Definir la ruta según el tipo de documento
    tipo_doc = comprobante_data['tipo_doc']
    tipo_doc_folder = 'factura' if tipo_doc == "01" else 'boleta'
    
    # Ruta donde se guardará el PDF
    output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', tipo_doc_folder, 
                                f"{tipo_doc}_{comprobante_data['numero_serie']}_{comprobante_data['correlativo']}.pdf")
    
    c = canvas.Canvas(output_path, pagesize=A4)  # Crear el canvas
    width, height = A4

    # Determinar si es boleta o factura para el manejo del IGV
    es_boleta = tipo_doc == "03"

    # Encabezado de VENTA: -------------------------------------------------------------------------------
    def draw_header(c):
        col_width = (width - 60) / 3
        y_position = height - 70

        # Parte 1:
        logo_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'daryza_logo.jpg')  # Ruta del logo
        c.drawImage(logo_path, 30, height - 87, width=87, height=50, preserveAspectRatio=True, mask='auto')

        # Parte 2:
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(20  + col_width + col_width / 50, y_position + 20, comprobante_data['razon_social'])
        c.setFont("Helvetica", 9)
        direccion = f"Dirección: {comprobante_data['urbanizacion']}, {comprobante_data['distrito']}, {comprobante_data['departamento']}"
        c.drawCentredString(20 + col_width + col_width / 50, y_position + 5, direccion)
        c.drawCentredString(20 + col_width + col_width / 50, y_position - 10, f"Email: {comprobante_data['email_empresa']}")

        # Parte 3:
        c.setFont("Helvetica-Bold", 10)
        titulo_venta = "BOLETA DE VENTA" if comprobante_data['tipo_doc'] == "03" else "FACTURA DE VENTA"
        c.drawCentredString(30 + 2 * col_width + col_width / 2, y_position + 20, titulo_venta)
        c.drawCentredString(30 + 2 * col_width + col_width / 2, y_position + 10, "ELECTRONICA")  # Añadir "ELECTRONICA"
        c.setFont("Helvetica", 10)
        numero_documento = f"{comprobante_data['numero_serie']}-{comprobante_data['correlativo']}"
        c.drawCentredString(30 + 2 * col_width + col_width / 2, y_position, numero_documento)
        c.drawCentredString(30 + 2 * col_width + col_width / 2, y_position - 10, f"RUC: {comprobante_data['empresa_ruc']}")
        # Rectángulo alrededor de la Parte 3
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.rect(30 + 2 * col_width, height - 98, col_width, 70)

    # Llamar a la función del encabezado
    draw_header(c)

    # Parte 2: Datos del cliente  -------------------------------------------------------------------------------
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 140, "Datos del Cliente:")
    cliente = comprobante_data['cliente']
    c.setFont("Helvetica", 9)
    if tipo_doc == "01":
        c.drawString(30, height - 155, f"RUC Cliente: {cliente['ruc_cliente']}")
        c.drawString(30, height - 170, f"Nombre/Razón Social: {cliente['razon_socialCliente']}")
        c.drawString(30, height - 185, f"Dirección: {cliente['direccion_clie']}")
    elif tipo_doc == "03":
        documento_cliente = "RUC" if comprobante_data['cliente_tipo_doc'] == "6" else "DNI"
        cliente_num_doc = cliente['ruc_cliente'] if comprobante_data['cliente_tipo_doc'] == "6" else cliente['dni_cliente']
        cliente_denominacion = cliente['razon_socialCliente'] if comprobante_data['cliente_tipo_doc'] == "6" else f"{cliente['nombre_clie']} {cliente['apellido_clie']}"
        c.drawString(30, height - 155, f"{documento_cliente} Cliente: {cliente_num_doc}")
        c.drawString(30, height - 170, f"Nombre/Razón Social: {cliente_denominacion}")
        c.drawString(30, height - 185, f"Dirección: {cliente['direccion_clie']}")
    c.setFont("Helvetica", 9)
    c.drawString(30, height - 210, f"Fecha de Emisión: {comprobante_data.get('fecha_emision', 'No disponible')}")
    c.drawString(30, height - 225, f"Hora de Emisión: {comprobante_data.get('hora_emision', 'No disponible')}")

    # Tabla de productos: -------------------------------------------------------------------------------
    y_position = height - 250  # Ajustar la posición vertical de la tabla
    detalle_data = comprobante_data['detalle']
    
    # Headers diferentes según si es boleta o factura
    if es_boleta:
        # Para boletas: no mostrar columna IGV separada, solo precio unitario
        table_data = [["ID", "DESCRIPCIÓN", "CANT.", "UNIDAD", "P. UNITARIO", "TOTAL"]]
        col_widths = [
            (width - 60) * 0.08,  # ID Producto
            (width - 60) * 0.35,  # Descripción (más espacio)
            (width - 60) * 0.10,  # Cantidad
            (width - 60) * 0.12,  # Unidad
            (width - 60) * 0.15,  # Precio Unitario
            (width - 60) * 0.20,  # Total
        ]
        for item in detalle_data:
            table_data.append([ 
                item['id_producto'],
                item['descripcion'],
                item['cantidad'],
                item['unidad'],
                f"{Decimal(item['monto_Precio_Unitario']):.2f}",  # Precio unitario (ya incluye IGV=0)
                f"{Decimal(item['monto_Valor_Venta']):.2f}",      # Total
            ])
    else:
        # Para facturas: mostrar todas las columnas incluido IGV
        table_data = [["ID", "DESCRIPCIÓN", "CANT.", "UNIDAD", "V. UNITARIO", "IGV", "P. UNIT"]]
        col_widths = [
            (width - 60) * 0.08,  # ID Producto
            (width - 60) * 0.25,  # Descripción
            (width - 60) * 0.09,  # Cantidad
            (width - 60) * 0.11,  # Unidad
            (width - 60) * 0.20,  # Valor Unitario
            (width - 60) * 0.08,  # IGV
            (width - 60) * 0.19,  # Precio Unitario
        ]
        for item in detalle_data:
            table_data.append([ 
                item['id_producto'],
                item['descripcion'],
                item['cantidad'],
                item['unidad'],
                f"{Decimal(item['monto_valorUnitario']):.2f}",
                f"{Decimal(item['igv_detalle']):.2f}",
                f"{Decimal(item['monto_Precio_Unitario']):.2f}",
            ])
        
    table = Table(table_data, colWidths=col_widths)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.wrapOn(c, width, height)
    table_height = table.wrap(width, height)[1]
    table.drawOn(c, 30, y_position - table_height)

    # Leyenda del comprobante:
    c.setFont("Helvetica-Bold", 9)
    legend_comprobante = comprobante_data.get('legend_comprobante')
    if legend_comprobante:
        legend_text = f"{legend_comprobante['legend_value']}"
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y_position - table_height - 60, "Leyenda:")
        c.setFont("Helvetica", 9)
        c.drawString(30, y_position - table_height - 75, legend_text)

    # Totales - diferentes según tipo de documento:
    c.setFont("Helvetica-Bold", 9)
    if es_boleta:
        # Para boletas: mostrar solo subtotal y total (IGV siempre es 0.00)
        c.drawString(425, y_position - table_height - 60, f"Subtotal: {comprobante_data['monto_Oper_Gravadas']}")
        c.drawString(425, y_position - table_height - 75, f"IGV (0%): 0.00")
        c.drawString(425, y_position - table_height - 90, f"Total: {comprobante_data['monto_Imp_Venta']}")
    else:
        # Para facturas: mostrar operaciones gravadas, IGV y total
        c.drawString(425, y_position - table_height - 60, f"Operaciones Gravadas: {comprobante_data['monto_Oper_Gravadas']}")
        c.drawString(425, y_position - table_height - 75, f"IGV (18%): {comprobante_data['monto_Igv']}")
        c.drawString(425, y_position - table_height - 90, f"Total: {comprobante_data['monto_Imp_Venta']}")

     # FOOTER PROFESIONAL E INDUSTRIAL - Cumpliendo estándares SUNAT:
    footer_y = 120  # Posición del footer
    
    # Línea superior del footer
    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.setLineWidth(2)
    c.line(30, footer_y + 20, width - 30, footer_y + 20)
    
    # Cuadro de representación impresa
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setLineWidth(1)
    c.rect(30, footer_y - 25, width - 60, 15)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(width / 2, footer_y - 18, "REPRESENTACIÓN IMPRESA DEL COMPROBANTE DE PAGO ELECTRÓNICO")
    
    # Información adicional de validación
    c.setFont("Helvetica", 6)
    c.drawString(30, footer_y - 40, f"Consulte la validez del documento en: www.sunat.gob.pe")
    c.drawRightString(width - 30, footer_y - 40, f"Documento procesado por sistema certificado")
    
    # Línea inferior
    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.setLineWidth(1)
    c.line(30, footer_y - 50, width - 30, footer_y - 50)

    c.save()
    return output_path