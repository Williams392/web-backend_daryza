import os
import zipfile
import base64
import logging
from pathlib import Path

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from lxml import etree
import xmlsec

# Configurar un logger para depuración
logger = logging.getLogger(__name__)

# --- CONSTANTES Y NAMESPACES ---
NS_MAP = {
    'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    'ds': "http://www.w3.org/2000/09/xmldsig#",
    'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
}
NS_INVOICE = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"

def _get_element(parent, tag, ns_key='cbc', text=None, attrs=None):
    """Función de ayuda para crear elementos XML con namespace y atributos."""
    el = etree.SubElement(parent, etree.QName(NS_MAP[ns_key], tag))
    if text is not None:
        el.text = str(text)
    if attrs:
        for key, value in attrs.items():
            el.set(key, value)
    return el


def generar_xml_factura(comprobante):
    """
    Genera el árbol XML para una factura o boleta en formato UBL 2.1.
    """
    # Raíz del documento (Invoice)
    root = etree.Element(etree.QName(NS_INVOICE, 'Invoice'), nsmap=NS_MAP)

    # --- UBL Version y Customization ID ---
    _get_element(root, 'UBLVersionID', text='2.1')
    _get_element(root, 'CustomizationID', text='2.0')

    # --- Datos del Comprobante ---
    _get_element(root, 'ID', text=f"{comprobante.numero_serie}-{comprobante.correlativo}")
    _get_element(root, 'IssueDate', text=comprobante.fecha_emision.strftime('%Y-%m-%d'))
    _get_element(root, 'IssueTime', text=comprobante.hora_emision.strftime('%H:%M:%S'))
    _get_element(root, 'InvoiceTypeCode', text=comprobante.tipo_doc,
                 attrs={'listID': comprobante.tipo_operacion, 'listAgencyName': 'PE:SUNAT',
                        'listName': 'Tipo de Documento', 'listURI': 'urn:pe:gob:sunat:cpe:see:gem:catalogos:catalogo01'})
    _get_element(root, 'Note', text=comprobante.legend_comprobante.legend_value, attrs={'languageLocaleID': '1000'})
    _get_element(root, 'DocumentCurrencyCode', text=comprobante.tipo_moneda, attrs={'listID': 'ISO 4217 Alpha', 'listName': 'Currency', 'listAgencyName': 'United Nations Economic Commission for Europe'})

    # --- Firma (Espacio reservado) ---
    signature = _get_element(root, 'Signature', 'cac')
    signature_id = _get_element(signature, 'ID', text=f"IDSign_{settings.SUNAT_RUC}")
    signatory_party = _get_element(signature, 'SignatoryParty', 'cac')
    party_identification = _get_element(signatory_party, 'PartyIdentification', 'cac')
    _ = _get_element(party_identification, 'ID', text=settings.SUNAT_RUC)
    party_name = _get_element(signatory_party, 'PartyName', 'cac')
    _ = _get_element(party_name, 'Name', text=comprobante.razon_social)
    digital_signature = _get_element(signature, 'DigitalSignatureAttachment', 'cac')
    external_reference = _get_element(digital_signature, 'ExternalReference', 'cac')
    _ = _get_element(external_reference, 'URI', text=f"#IDSign_{settings.SUNAT_RUC}")

    # 💥 Agrega el nodo <ds:Signature> vacío que será reemplazado por la firma digital
    etree.SubElement(root, etree.QName(NS_MAP['ds'], 'Signature'))

    # --- Datos del Emisor ---
    supplier = _get_element(root, 'AccountingSupplierParty', 'cac')
    party = _get_element(supplier, 'Party', 'cac')
    party_identification = _get_element(party, 'PartyIdentification', 'cac')
    _get_element(party_identification, 'ID', text=comprobante.empresa_ruc, attrs={'schemeID': '6'})
    party_legal_entity = _get_element(party, 'PartyLegalEntity', 'cac')
    _get_element(party_legal_entity, 'RegistrationName', text=comprobante.razon_social)
    registration_address = _get_element(party_legal_entity, 'RegistrationAddress', 'cac')
    _get_element(registration_address, 'AddressTypeCode', text='0000') # Domicilio Fiscal

    # --- Datos del Receptor (Cliente) ---
    customer = _get_element(root, 'AccountingCustomerParty', 'cac')
    party = _get_element(customer, 'Party', 'cac')
    party_identification = _get_element(party, 'PartyIdentification', 'cac')
    num_doc_cliente = comprobante.cliente.ruc_cliente if comprobante.cliente_tipo_doc == '6' else comprobante.cliente.dni_cliente
    _get_element(party_identification, 'ID', text=num_doc_cliente, attrs={'schemeID': comprobante.cliente_tipo_doc})
    party_legal_entity = _get_element(party, 'PartyLegalEntity', 'cac')
    razon_social_cliente = comprobante.cliente.razon_socialCliente if comprobante.cliente_tipo_doc == '6' else f"{comprobante.cliente.nombre_clie} {comprobante.cliente.apellido_clie}"
    _get_element(party_legal_entity, 'RegistrationName', text=razon_social_cliente)

    # --- Totales de Impuestos ---
    tax_total = _get_element(root, 'TaxTotal', 'cac')
    _get_element(tax_total, 'TaxAmount', text=f"{comprobante.monto_Igv:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
    tax_subtotal = _get_element(tax_total, 'TaxSubtotal', 'cac')
    _get_element(tax_subtotal, 'TaxableAmount', text=f"{comprobante.monto_Oper_Gravadas:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
    _get_element(tax_subtotal, 'TaxAmount', text=f"{comprobante.monto_Igv:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
    tax_category = _get_element(tax_subtotal, 'TaxCategory', 'cac')
    tax_scheme = _get_element(tax_category, 'TaxScheme', 'cac')
    _get_element(tax_scheme, 'ID', text='1000')
    _get_element(tax_scheme, 'Name', text='IGV')
    _get_element(tax_scheme, 'TaxTypeCode', text='VAT')

    # --- Total del Comprobante ---
    legal_monetary_total = _get_element(root, 'LegalMonetaryTotal', 'cac')
    _get_element(legal_monetary_total, 'LineExtensionAmount', text=f"{comprobante.monto_Oper_Gravadas:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
    _get_element(legal_monetary_total, 'TaxInclusiveAmount', text=f"{comprobante.monto_Imp_Venta:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
    _get_element(legal_monetary_total, 'PayableAmount', text=f"{comprobante.monto_Imp_Venta:.2f}", attrs={'currencyID': comprobante.tipo_moneda})

    # --- Líneas de Detalle ---
    for i, detalle in enumerate(comprobante.detalle.all(), start=1):
        line = _get_element(root, 'InvoiceLine', 'cac')
        _get_element(line, 'ID', text=str(i))
        _get_element(line, 'InvoicedQuantity', text=str(detalle.cantidad), attrs={'unitCode': detalle.unidad})
        _get_element(line, 'LineExtensionAmount', text=f"{detalle.monto_Valor_Venta:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
        
        pricing_reference = _get_element(line, 'PricingReference', 'cac')
        alt_condition_price = _get_element(pricing_reference, 'AlternativeConditionPrice', 'cac')
        _get_element(alt_condition_price, 'PriceAmount', text=f"{detalle.monto_Precio_Unitario:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
        _get_element(alt_condition_price, 'PriceTypeCode', text='01')

        tax_total_line = _get_element(line, 'TaxTotal', 'cac')
        _get_element(tax_total_line, 'TaxAmount', text=f"{detalle.igv_detalle:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
        tax_subtotal_line = _get_element(tax_total_line, 'TaxSubtotal', 'cac')
        _get_element(tax_subtotal_line, 'TaxableAmount', text=f"{detalle.monto_Valor_Venta:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
        _get_element(tax_subtotal_line, 'TaxAmount', text=f"{detalle.igv_detalle:.2f}", attrs={'currencyID': comprobante.tipo_moneda})
        tax_category_line = _get_element(tax_subtotal_line, 'TaxCategory', 'cac')
        _get_element(tax_category_line, 'Percent', text='18.00')
        _get_element(tax_category_line, 'TaxExemptionReasonCode', text='10')
        tax_scheme_line = _get_element(tax_category_line, 'TaxScheme', 'cac')
        _get_element(tax_scheme_line, 'ID', text='1000')
        _get_element(tax_scheme_line, 'Name', text='IGV')
        _get_element(tax_scheme_line, 'TaxTypeCode', text='VAT')

        item = _get_element(line, 'Item', 'cac')
        _get_element(item, 'Description', text=detalle.descripcion)
        sellers_item_id = _get_element(item, 'SellersItemIdentification', 'cac')
        _get_element(sellers_item_id, 'ID', text=detalle.id_producto)
        
        price = _get_element(line, 'Price', 'cac')
        _get_element(price, 'PriceAmount', text=f"{detalle.monto_valorUnitario:.2f}", attrs={'currencyID': comprobante.tipo_moneda})

    return root

def firmar_xml(xml_tree):
    """
    Firma un árbol XML utilizando el certificado digital configurado.
    """
    # El nodo a firmar es el propio documento
    reference_node = xml_tree
    
    # El nodo donde se insertará la firma
    signature_node = xml_tree.find('.//ds:Signature', namespaces=NS_MAP)
    if signature_node is None:
        raise Exception("No se encontró el nodo ds:Signature en el XML.")

    # Cargar la clave privada del certificado
    try:
        ctx = xmlsec.SignatureContext()
        #key = xmlsec.Key.from_file(settings.CERTIFICADO_DIGITAL_PATH, xmlsec.KeyFormat.PKCS12, settings.CERTIFICADO_DIGITAL_PASS)
        key = xmlsec.Key.from_file(settings.CERTIFICADO_DIGITAL_PATH, xmlsec.KeyFormat.PEM, None)
        ctx.key = key
        
        # Firmar el documento
        ctx.sign(signature_node, reference_node)
    except Exception as e:
        logger.error(f"Error al firmar el XML: {e}")
        raise
        
    return xml_tree

def enviar_documento_sunat(xml_firmado_str, nombre_archivo):
    """
    Envía el documento XML firmado a la SUNAT.
    """
    try:
        # 1. Comprimir el XML en un archivo ZIP
        zip_buffer = Path(f'/tmp/{nombre_archivo}.zip')
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f'{nombre_archivo}.xml', xml_firmado_str)
        
        # 2. Codificar el ZIP en Base64
        with open(zip_buffer, 'rb') as f:
            zip_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # 3. Construir el sobre SOAP para el envío
        soap_request = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.sunat.gob.pe" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <soapenv:Header>
                <wsse:Security>
                    <wsse:UsernameToken>
                        <wsse:Username>{settings.SUNAT_RUC}{settings.SUNAT_USUARIO_SOL}</wsse:Username>
                        <wsse:Password>{settings.SUNAT_CLAVE_SOL}</wsse:Password>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <ser:sendBill>
                    <fileName>{nombre_archivo}.zip</fileName>
                    <contentFile>{zip_base64}</contentFile>
                </ser:sendBill>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        
        # 4. Realizar la petición POST a la SUNAT
        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        response = requests.post(settings.SUNAT_API_URL, data=soap_request.encode('utf-8'), headers=headers, timeout=30)
        
        # 5. Procesar la respuesta
        if response.status_code == 200:
            soap_response_tree = etree.fromstring(response.content)
            cdr_base64 = soap_response_tree.find('.//applicationResponse').text
            cdr_data = base64.b64decode(cdr_base64)
            
            # Guardar el CDR
            cdr_zip_path = f'/tmp/R-{nombre_archivo}.zip'
            with open(cdr_zip_path, 'wb') as f:
                f.write(cdr_data)
            
            # Extraer el XML del CDR para obtener la respuesta
            with zipfile.ZipFile(cdr_zip_path, 'r') as zf:
                cdr_xml_filename = [name for name in zf.namelist() if name.upper().endswith('.XML')][0]
                cdr_xml_content = zf.read(cdr_xml_filename)
            
            cdr_tree = etree.fromstring(cdr_xml_content)
            response_code = cdr_tree.find('.//cbc:ResponseCode', namespaces=NS_MAP).text
            description = cdr_tree.find('.//cbc:Description', namespaces=NS_MAP).text
            
            estado = "ACEPTADO" if response_code == "0" else "RECHAZADO"
            
            return {
                "success": True,
                "cdr_data": cdr_data,
                "cdr_filename": f"R-{nombre_archivo}.zip",
                "estado_sunat": estado,
                "respuesta_sunat": description
            }
        else:
            logger.error(f"Error en la comunicación con SUNAT: {response.status_code} - {response.text}")
            return {"success": False, "respuesta_sunat": response.text}

    except Exception as e:
        logger.error(f"Excepción al enviar a SUNAT: {e}")
        return {"success": False, "respuesta_sunat": str(e)}
    finally:
        # Limpiar archivos temporales
        if 'zip_buffer' in locals() and os.path.exists(zip_buffer):
            os.remove(zip_buffer)
        if 'cdr_zip_path' in locals() and os.path.exists(cdr_zip_path):
            os.remove(cdr_zip_path)


def procesar_venta_electronica(comprobante):
    """
    Orquesta todo el proceso: genera XML, firma, envía y actualiza el modelo.
    """
    try:
        # 1. Generar el nombre del archivo
        # Formato: RUC-TIPO_DOC-SERIE-CORRELATIVO
        nombre_archivo = f"{comprobante.empresa_ruc}-{comprobante.tipo_doc}-{comprobante.numero_serie}-{comprobante.correlativo}"

        # 2. Generar el XML sin firmar
        xml_tree = generar_xml_factura(comprobante)
        
        # 3. Firmar el XML
        xml_firmado_tree = firmar_xml(xml_tree)
        xml_firmado_str = etree.tostring(xml_firmado_tree, pretty_print=True, xml_declaration=True, encoding='utf-8')
        
        # Guardar el XML firmado en el modelo
        comprobante.xml_enviado_url.save(f"{nombre_archivo}.xml", ContentFile(xml_firmado_str), save=False)

        # 4. Enviar a SUNAT
        resultado = enviar_documento_sunat(xml_firmado_str, nombre_archivo)

        # 5. Actualizar el modelo con la respuesta
        if resultado["success"]:
            comprobante.cdr_sunat_url.save(resultado["cdr_filename"], ContentFile(resultado["cdr_data"]), save=False)
            comprobante.estado_sunat = resultado["estado_sunat"]
            comprobante.respuesta_sunat = resultado["respuesta_sunat"]
            logger.info(f"Comprobante {nombre_archivo} procesado. Estado: {resultado['estado_sunat']}")
        else:
            comprobante.estado_sunat = "ERROR"
            comprobante.respuesta_sunat = resultado["respuesta_sunat"]
            logger.error(f"Fallo al procesar {nombre_archivo}: {resultado['respuesta_sunat']}")
        
        comprobante.save()

    except Exception as e:
        # Si algo falla en el proceso, registrar el error en el modelo
        nombre_archivo = f"{comprobante.empresa_ruc}-{comprobante.tipo_doc}-{comprobante.numero_serie}-{comprobante.correlativo}"
        logger.critical(f"Error CRÍTICO al procesar el comprobante {nombre_archivo}: {e}", exc_info=True)
        comprobante.estado_sunat = "ERROR_INTERNO"
        comprobante.respuesta_sunat = str(e)
        comprobante.save()
