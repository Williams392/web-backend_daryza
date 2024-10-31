from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from django.conf import settings
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

    # Parte 1 de la empresa:
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'daryza_logo.jpg')  # Ruta del logo
    c.drawImage(logo_path, 30, height - 80, width=80, height=40, preserveAspectRatio=True, mask='auto')
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(120, height - 60, comprobante_data['razon_social'])
    c.setFont("Helvetica", 9)
    direccion = f"Dirección: {comprobante_data['urbanizacion']}, {comprobante_data['distrito']}, {comprobante_data['departamento']}"
    c.drawString(120, height - 75, direccion)
    c.drawString(120, height - 90, f"Email: {comprobante_data['email_empresa']}")

    # Título de venta
    c.setFont("Helvetica-Bold", 16)  
    titulo_venta = "BOLETA DE VENTA" if comprobante_data['tipo_doc'] == "03" else "FACTURA"
    c.drawString(350, height - 60, titulo_venta)
    
    c.setFont("Helvetica-Bold", 14)
    numero_documento = f"{comprobante_data['numero_serie']}-{comprobante_data['correlativo']}"
    c.drawString(350, height - 85, numero_documento)  
    c.drawString(350, height - 100, f"RUC: {comprobante_data['empresa_ruc']}")

    # Parte 2: Datos del cliente
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 140, "Datos del Cliente:")

    cliente = comprobante_data['cliente']  # cliente es un diccionario en este caso

    c.setFont("Helvetica", 9)
    if tipo_doc == "01":
        # Para facturas, solo muestra RUC del cliente, denominación y dirección
        c.drawString(30, height - 155, f"RUC Cliente: {cliente['ruc_cliente']}")
        c.drawString(30, height - 170, f"Nombre/Razón Social: {cliente['razon_socialCliente']}")
        c.drawString(30, height - 185, f"Dirección: {cliente['direccion_clie']}")
    elif tipo_doc == "03":
        # Para boletas, muestra RUC o DNI del cliente según `cliente_tipo_doc`
        documento_cliente = "RUC" if comprobante_data['cliente_tipo_doc'] == "6" else "DNI"
        cliente_num_doc = cliente['ruc_cliente'] if comprobante_data['cliente_tipo_doc'] == "6" else cliente['dni_cliente']
        cliente_denominacion = cliente['razon_socialCliente'] if comprobante_data['cliente_tipo_doc'] == "6" else f"{cliente['nombre_clie']} {cliente['apellido_clie']}"

        c.drawString(30, height - 155, f"{documento_cliente} Cliente: {cliente_num_doc}")
        c.drawString(30, height - 170, f"Nombre/Razón Social: {cliente_denominacion}")
        c.drawString(30, height - 185, f"Dirección: {cliente['direccion_clie']}")

    # Añade la fecha y hora de emisión
    c.setFont("Helvetica", 9)
    c.drawString(30, height - 210, f"Fecha de Emisión: {comprobante_data.get('fecha_emision', 'No disponible')}")
    c.drawString(30, height - 225, f"Hora de Emisión: {comprobante_data.get('hora_emision', 'No disponible')}")

    c.save()
    return output_path

    return output_path
