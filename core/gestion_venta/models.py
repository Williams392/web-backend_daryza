from django.db import models
from django.core.validators import EmailValidator
from gestion_almacen.models import Producto
from authentication.models import CustomUser
import uuid


class Empresa(models.Model):  # EMISOR
    id_empresa = models.AutoField(primary_key=True)
    ruc_empresa = models.CharField(max_length=11, null=False, blank=True)
    razon_social = models.CharField(max_length=50, null=False)  # nombre de la empresa
    nombre_comercial = models.CharField(max_length=200, null=True, blank=True)
    tipo_empresa = models.CharField(max_length=100, null=True, blank=False)  
    ubigeo = models.CharField(max_length=100, null=True, blank=True)

    urbanizacion = models.CharField(max_length=200, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    email_empresa = models.EmailField(max_length=50, validators=[EmailValidator()], null=True, blank=True)
    telefono_emp = models.CharField(max_length=50, null=True, blank=True)

    logo = models.ImageField(upload_to='logo/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_empresa'

    def __str__(self):
        return f"{self.nombre_comercial} {self.ruc_empresa}"



class Cliente(models.Model):  # RECEPTOR
    id_cliente = models.AutoField(primary_key=True)
    nombre_clie = models.CharField(max_length=255, null=False, blank=True)
    apellido_clie = models.CharField(max_length=255, null=True, blank=True)
    
    #cliente_tipo_doc = models.CharField(max_length=3, null=True)  # Aquí defines el valor por defecto # 8 - DNI, 6 - RUC
    dni_cliente = models.CharField(max_length=8, null=True, blank=True, unique=True)  # Aquí defines el valor por defecto # 8 - DNI, 6 - RUC
    ruc_cliente = models.CharField(max_length=11, null=True, blank=True, unique=True)  # Aquí defines el valor por defecto
    
    #cliente_numDoc = models.CharField(max_length=11, null=True, blank=True, unique=True)  # Aquí defines el valor por defecto # 8 - DNI, 6 - RUC
    
    direccion_clie = models.CharField(max_length=255, null=True, blank=True)
    razon_socialCliente = models.CharField(max_length=255, null=True, blank=True)

    tipo_empresa = models.CharField(max_length=255, null=True, blank=True)
    email_cliente = models.EmailField(max_length=50, validators=[EmailValidator()], null=True, blank=True)
    telefono_cliente = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'tb_cliente'

    
class Legend(models.Model):
    id_legend = models.AutoField(primary_key=True)
    #comprobante = models.ForeignKey(Comprobante, related_name='legend', on_delete=models.CASCADE)
    legend_code = models.CharField(max_length=4)
    legend_value = models.TextField()

    class Meta:
        db_table = 'tb_legend'

class FormaPago(models.Model): # contado, credito, efectivo.
    id_formaPago = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10)
    monto = models.IntegerField(default=0)
    cuota = models.IntegerField(default=0)
    fecha_pago = models.DateTimeField()
    class Meta:
        db_table = 'tb_forma_pago'

class DetalleComprobante(models.Model):
    id_detalleComprobante = models.AutoField(primary_key=True)

    unidad = models.CharField(max_length=6, null=False)
    cantidad = models.PositiveIntegerField()
    cod_producto = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=255)

    monto_valorUnitario = models.FloatField(default=0)
    igv_detalle = models.FloatField(default=0)

    fecha_emision = models.DateField(auto_now_add=True)  # Solo la fecha
    hora_emision = models.TimeField(auto_now_add=True)  # Solo la hora

    total_Impuestos = models.FloatField(default=0)
    monto_Precio_Unitario = models.FloatField(default=0)
    monto_Valor_Venta = models.FloatField(default=0)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True) # obtener unidad
    
    class Meta:
        db_table = 'tb_detalle_comprobante'

# Boleta comienza con B001 - Factura comienza con F001
class Comprobante(models.Model):
    uuid_comprobante = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    tipo_operacion = models.CharField(max_length=4)   # Catálogo No. 51
    tipo_doc = models.CharField(max_length=3)  # Boleta - Factura
    numero_serie = models.CharField(max_length=4) # maximo 4 - sunat(B001 - F001)
    correlativo = models.CharField(max_length=10) # 1
    tipo_moneda = models.CharField(max_length=3)  # PEN - DOL
    fecha_emision = models.DateField(auto_now_add=True)  # Solo la fecha
    hora_emision = models.TimeField(auto_now_add=True)  # Solo la hora

    empresa_ruc = models.CharField(max_length=11)

    cliente_tipo_doc = models.CharField(max_length=11)
    cliente_num_doc = models.CharField(max_length=11)
    cliente_razon_social = models.CharField(max_length=255)
    cliente_direccion = models.TextField(max_length=255)

    monto_Oper_Gravadas = models.IntegerField(default=0)
    monto_Igv = models.IntegerField(default=0)
    valor_venta = models.IntegerField(default=0)
    total_impuestos = models.IntegerField(default=0)
    sub_Total = models.IntegerField(default=0)
    monto_Imp_Venta = models.IntegerField(default=0)
   
    estado_Documento = models.CharField(max_length=1, default='0')  # si es 0 esta pendiente el documento, enviado, aceptado, rechazado.
    manual = models.BooleanField(default=False)  # si es false significa que el documento fue generado automaticamente por el sistema.
    
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE, null=True)
    legend_comprobante = models.ForeignKey(Legend, on_delete=models.CASCADE, null=True)
    detalle = models.ForeignKey(DetalleComprobante, on_delete=models.CASCADE, null=True)

    emisor = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    receptor = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'tb_comprobante'







# Envió de Boleta y Factura:
# https://docs.factiliza.com/apis/api-sunat-facturacion/facturas-y-boletas/envio-documento


# No en uso:
# class Impuesto(models.Model):  # IMPUESTO ( Gravado - Exonerado - Inafecto)
#     id_impuesto = models.AutoField(primary_key=True)
#     nombre_impuesto = models.CharField(max_length=50)
#     porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

#     class Meta:
#         db_table = 'tb_impuesto'

#     def __str__(self):
#         return f"{self.nombre_impuesto} ({self.porcentaje}%)"


# class TipoComprobante(models.Model):
#     id_tipoComprobante = models.AutoField(primary_key=True)
#     nombre_tipo = models.CharField(max_length=4)

#     class Meta:
#         db_table = 'tb_tipo_comprobante'

#     def __str__(self):
#         return self.nombre_tipo

  
# class EstadoComprobante(models.Model):
#     id_estadoComprobante = models.AutoField(primary_key=True)
#     nombre_estado = models.CharField(max_length=50)
#     detalles = models.TextField(null=True, blank=True) 

#     class Meta:
#         db_table = 'tb_estado_comprobante'

#     def __str__(self):
#         return self.nombre_estado