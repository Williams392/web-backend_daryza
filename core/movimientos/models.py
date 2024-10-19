from django.db import models
from gestion_almacen.models import Producto
from authentication.models import CustomUser
import uuid

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50, null=True)
    telf_suc = models.CharField(max_length=20)
    correo_suc = models.CharField(max_length=25)
    direccion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class TipoMovimiento(models.Model): # Entrada oh Salida
    id_tipoMovimiento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        db_table = 'tb_tipoMovimiento'

class Movimiento(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    #uuid_movimiento = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    serie = models.CharField(max_length=7, unique=True)
    correlativo = models.CharField(max_length=5, unique=True)
    fecha = models.DateField()
    fecha_entrega = models.DateField()
    referencia = models.CharField(max_length=50, null=True)
    cant_total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE) # lo cambie por 
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)

    def __str__(self):
        return self.serie

    class Meta:
        db_table = 'tb_movimiento'

class DetalleMovimiento(models.Model):
    id_detalleMovimiento = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_detalleMovimiento'
