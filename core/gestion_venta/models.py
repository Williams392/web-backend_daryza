from django.db import models
from django.core.validators import EmailValidator
from gestion_almacen.models import Producto
from authentication.models import CustomUser
import uuid

class Empresa(models.Model):  # EMISOR
    id_empresa = models.AutoField(primary_key=True)
    ruc_empresa = models.CharField(max_length=11, null=True, blank=True)
    razon_social = models.CharField(max_length=50)  # nombre de la empresa
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
    nombre_clie = models.CharField(max_length=255, null=True, blank=True)
    apellido_clie = models.CharField(max_length=255, null=True, blank=True)
    direccion_clie = models.CharField(max_length=255, null=True, blank=True)
    razon_socialCliente = models.CharField(max_length=255, null=True, blank=True)
    tipo_empresa = models.CharField(max_length=255, null=True, blank=True)
    email_cliente = models.EmailField(max_length=50, validators=[EmailValidator()], null=True, blank=True)
    telefono_cliente = models.CharField(max_length=20, null=True, blank=True)
    ruc_cliente = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        db_table = 'tb_cliente'


class Impuesto(models.Model):  # IMPUESTO
    id_impuesto = models.AutoField(primary_key=True)
    nombre_impuesto = models.CharField(max_length=50)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'tb_impuesto'

    def __str__(self):
        return f"{self.nombre_impuesto} ({self.porcentaje}%)"


class EstadoComprobante(models.Model):
    id_estadoComprobante = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)
    detalles = models.TextField(null=True, blank=True) 

    class Meta:
        db_table = 'tb_estado_comprobante'

    def __str__(self):
        return self.nombre_estado

class TipoComprobante(models.Model):
    id_tipoComprobante = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=4)

    class Meta:
        db_table = 'tb_tipo_comprobante'

    def __str__(self):
        return self.nombre_tipo
    

# Boleta comienza con B001 - Factura comienza con F001
class Comprobante(models.Model):
    uuid_comprobante = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    tipo_operacion = models.CharField(max_length=3)  # Catálogo No. 01
    tipo_doc = models.CharField(max_length=3)  # B001
    numero_serie = models.CharField(max_length=4) # maximo 4 - sunat
    correlativo = models.CharField(max_length=10)
    tipo_moneda = models.CharField(max_length=3)  

    fecha_emision = models.DateField(auto_now_add=True)  # Solo la fecha
    hora_emision = models.TimeField(auto_now_add=True)  # Solo la hora

    empresa_ruc = models.CharField(max_length=11)

    cliente_tipo_doc = models.CharField(max_length=11)
    cliente_num_doc = models.CharField(max_length=11)
    cliente_razon_social = models.CharField(max_length=255)
    cliente_direccion = models.TextField()

    mto_operGravadas = models.FloatField(default=0.0)
    mto_igv = models.FloatField(default=0.0)
    valor_venta = models.FloatField(default=0.0)
    total_impuestos = models.DecimalField(max_digits=10, decimal_places=2)
    sub_totalVenta = models.FloatField(default=0.0)
    mto_importeTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Asociación:
    tipo = models.ForeignKey(TipoComprobante, on_delete=models.CASCADE) # '01' para factura, '02' para boleta
    emisor = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    receptor = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    impuestos = models.ForeignKey(Impuesto, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoComprobante, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tb_comprobante'

    def save(self, *args, **kwargs): # arreglar:
        self.total = sum(item.cantidad * item.precio_unitario for item in self.items.all())
        super().save(*args, **kwargs)


class DetalleComprobante(models.Model):
    uuid_detalleComprobante = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    unidad = models.CharField(max_length=6)
    cantidad = models.PositiveIntegerField()
    cod_producto = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=255)

    mto_valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    mto_valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    igv_detalle = models.DecimalField(max_digits=10, decimal_places=2)

    fecha_emision = models.DateField(auto_now_add=True)  # Solo la fecha
    hora_emision = models.TimeField(auto_now_add=True)  # Solo la hora

    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # obtener unidad
    
    class Meta:
        db_table = 'tb_detalle_comprobante'

    def __str__(self):
        return f"{self.producto.nombre_prod} - {self.cantidad} unidades a {self.mto_valorUnitario} cada una"
 
class Legend(models.Model):
    id_legend = models.AutoField(primary_key=True)
    comprobante = models.ForeignKey(Comprobante, related_name='legend', on_delete=models.CASCADE)
    legend_code = models.CharField(max_length=4)
    legend_value = models.TextField()

    class Meta:
        db_table = 'tb_legend'

class FormaPago(models.Model): # credito, efectivo.
    id_formaPago = models.AutoField(primary_key=True)
    comprobante = models.ForeignKey(Comprobante, related_name='forma_pago', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cuota = models.IntegerField()
    fecha_pago = models.DateTimeField()
    class Meta:
        db_table = 'tb_forma_pago'