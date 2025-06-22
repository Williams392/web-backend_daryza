from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from core.models import TimeStampedModel

class Categoria(TimeStampedModel):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100, unique=True)
    estado_categoria = models.BooleanField(default=True)

    class Meta:
        db_table = 'tb_categoria'

    def __str__(self):
        return self.nombre_categoria
    
    def clean(self):
        if not self.nombre_categoria:
            raise ValidationError('El nombre de la marca no puede estar vacío.')

class Marca(TimeStampedModel):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=100, unique=True)
    estado_marca = models.BooleanField(default=True)

    class Meta:
        db_table = 'tb_marca'

    def __str__(self):
        return self.nombre_marca

    def clean(self):
        if not self.nombre_marca:
            raise ValidationError('El nombre de la marca no puede estar vacío.')


class UnidadMedida(TimeStampedModel):
    id_unidadMedida = models.AutoField(primary_key=True)
    nombre_unidad = models.CharField(max_length=100, unique=True)
    abreviacion = models.CharField(max_length=100, unique=True)
    estado_unidad = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_unidad}"
    
    class Meta:
        db_table = 'tb_unidadMedida'


class Producto(TimeStampedModel):
    id_producto = models.AutoField(primary_key=True)
    nombre_prod = models.CharField(max_length=100, unique=True)
    descripcion_pro = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    codigo = models.CharField(max_length=100, unique=True) 
    estado = models.BooleanField(default=True)
    estock = models.IntegerField()
    estock_minimo = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)

    class Meta:
        db_table = 'tb_producto'

    def __str__(self):
        return f"{self.nombre_prod}"
    
    def mostrar_imagen(self): 
        if self.imagen:
            return format_html('<img src="{}" width="100" height="100" />'.format(self.imagen.url))
        else:
            return ''
        
    mostrar_imagen.short_description = 'Imagen' # dar un titulo ala tabla

    