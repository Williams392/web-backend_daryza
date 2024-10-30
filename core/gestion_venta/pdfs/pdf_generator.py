# gestion_ventas/pdfs/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from django.conf import settings
import os

def generar_pdf_comprobante(comprobante_data):
    # Ruta donde se guardará el PDF
    output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', f"{comprobante_data['tipo_doc']}_{comprobante_data['numero_serie']}_{comprobante_data['correlativo']}.pdf")

    # Crear el canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Ruta del logo
    logo_path = os.path.join(settings.BASE_DIR, 'media/logo/daryza_logo.jpg')

    # Encabezado con logo
    c.drawImage(logo_path, 2 * cm, height - 4 * cm, width=4 * cm, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold", 12)
    c.drawString(7 * cm, height - 2 * cm, comprobante_data['razon_social'])
    c.setFont("Helvetica", 10)
    c.drawString(7 * cm, height - 2.5 * cm, f"RUC: {comprobante_data['empresa_ruc']}")
    c.drawString(7 * cm, height - 3 * cm, f"Dirección: {comprobante_data['urbanizacion']}, {comprobante_data['distrito']}, {comprobante_data['departamento']}")
    c.drawString(7 * cm, height - 3.5 * cm, f"Email: {comprobante_data['email_empresa']} Tel: {comprobante_data['telefono_emp']}")

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 5 * cm, "BOLETA DE VENTA" if comprobante_data['tipo_doc'] == "03" else "FACTURA")

    # Información del cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, height - 6 * cm, "Cliente:")
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 6.5 * cm, f"Nombre: {comprobante_data['cliente']['cliente_denominacion']}")
    c.drawString(2 * cm, height - 7 * cm, f"DNI/RUC: {comprobante_data['cliente']['cliente_num_doc']}")
    c.drawString(2 * cm, height - 7.5 * cm, f"Dirección: {comprobante_data['cliente']['cliente_direccion']}")

    # Detalles de la venta
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, height - 9 * cm, "Detalles de la Venta:")
    c.setFont("Helvetica", 10)
    y = height - 10 * cm
    for detalle in comprobante_data['detalle']:
        c.drawString(2 * cm, y, f"{detalle['descripcion']} - Cantidad: {detalle['cantidad']} - Precio Unitario: {detalle['monto_Precio_Unitario']} - Total: {detalle['monto_Valor_Venta']}")
        y -= 0.5 * cm

    # Totales
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y - 1 * cm, f"Subtotal: {comprobante_data['valor_venta']}")
    c.drawString(2 * cm, y - 1.5 * cm, f"IGV: {comprobante_data['monto_Igv']}")
    c.drawString(2 * cm, y - 2 * cm, f"Total: {comprobante_data['monto_Imp_Venta']}")

    # Guardar el PDF
    c.save()

    return output_path
