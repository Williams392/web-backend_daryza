from django.db import models
from gestion_venta.models import *
from gestion_venta.models import Producto
from authentication.models import CustomUser
import uuid

# class Auditoria(models.Model):
#     codigo_au = models.AutoField(primary_key=True)
#     usuario_au = models.CharField(max_length=128, null=False)
#     tabla = models.CharField(max_length=50)
#     accion = models.CharField(max_length=20)
#     registro = models.CharField(max_length=20)
#     nombre = models.CharField(max_length=100)
#     descripcion = models.CharField(max_length=50, blank=True, null=True)
#     fecha_hora = models.DateTimeField()

#     class Meta:
#         db_table = 'Auditoria'

#     def __str__(self):
#         return f"{self.nombre} - {self.accion} - {self.fecha_hora}"
    
    
class TipoMovimiento(models.Model): # Entrada oh Salida
    id_tipoMovimiento = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        db_table = 'tb_tipoMovimiento'

class Movimiento(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    referencia = models.CharField(max_length=50, null=True)
    cant_total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE) # lo cambie por 
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)

    def __str__(self):
        return self.referencia

    class Meta:
        db_table = 'tb_movimiento'

class DetalleMovimiento(models.Model):
    id_detalleMovimiento = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    detalleComprobante = models.ForeignKey(DetalleComprobante, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'tb_detalleMovimiento'


