from django.db import models
from django.core.validators import EmailValidator
from gestion_almacen.models import Producto
import uuid

class Empresa(models.Model):  # EMPRESA
    uuid_empresa = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ruc_empresa = models.CharField(max_length=200, null=True, blank=True)
    razon_social = models.CharField(max_length=50)  # nombre de la empresa
    nombre_comercial = models.CharField(max_length=200, null=True, blank=True)
    tipo_empresa = models.CharField(max_length=100, null=True, blank=False)  
    ubigeo = models.CharField(max_length=100, null=True, blank=True)

    urbanizacion = models.CharField(max_length=200, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)

    email_empresa = models.EmailField(max_length=50, validators=[EmailValidator()], null=True, blank=True)
    telefono_1 = models.CharField(max_length=50, null=True, blank=True)
    telefono_2 = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tb_empresa'

    def __str__(self):
        return f"{self.nombre_comercial} {self.ruc_empresa}"


class Cliente(models.Model):  # CLIENTE
    uuid_cliente = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True)
    apellido_cliente = models.CharField(max_length=255, null=True, blank=True)
    direccion_cliente = models.CharField(max_length=255, null=True, blank=True)
    razon_social_cliente = models.CharField(max_length=255, null=True, blank=True)
    tipo_empresa = models.CharField(max_length=255, null=True, blank=True)
    email_cliente = models.CharField(max_length=255, null=True, blank=True)
    telefono_1 = models.CharField(max_length=20, null=True, blank=True)
    telefono_2 = models.CharField(max_length=20, null=True, blank=True)
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
    
class FormaPago(models.Model):
    id_formaPago = models.AutoField(primary_key=True)
    nombre_fromaPago = models.CharField(max_length=50)
    detalles = models.TextField(null=True, blank=True)  
    class Meta:
        db_table = 'tb_forma_pago'
    
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
    nombre_tipo = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_tipo_comprobante'

    def __str__(self):
        return self.nombre_tipo

class Comprobante(models.Model):
    uuid_comprobante = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    numero_serie = models.CharField(max_length=4) # maximo 4 - sunat
    correlativo = models.CharField(max_length=10)
    fecha_emision = models.DateField(auto_now_add=True)  # Solo la fecha
    hora_emision = models.TimeField(auto_now_add=True)  # Solo la hora
    forma_pago = models.CharField(max_length=50)
    
    # Asociación:
    tipo = models.ForeignKey(TipoComprobante, on_delete=models.CASCADE)
    emisor = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    receptor = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    items = models.ManyToManyField(Producto)
    impuestos = models.ManyToManyField(Impuesto)
    
    importe_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        db_table = 'tb_comprobante'

    def save(self, *args, **kwargs):
        self.total = sum(item.cantidad * item.precio_unitario for item in self.items.all())
        super().save(*args, **kwargs)


class DetalleComprobante(models.Model):
    uuid_detalleComprobante = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_detalle_comprobante'

    def __str__(self):
        return f"{self.producto.nombre_prod} - {self.cantidad} unidades a {self.precio_unitario} cada una"
    