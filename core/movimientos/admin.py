from django.contrib import admin
from .models import *
from django.db import models

# Register your models here.

class AudotoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario_au', 'tabla', 'accion', 'fecha_hora')
    
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id_movimiento', 'referencia', 'cant_total', 'tipo_movimiento', 'created_at')

class DetalleMovimientoAdmin(admin.ModelAdmin):
    list_display = ('movimiento', 'producto', 'cantidad')

class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)

# admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Auditoria, AudotoriaAdmin)
admin.site.register(Movimiento, MovimientoAdmin)
admin.site.register(DetalleMovimiento, DetalleMovimientoAdmin)
admin.site.register(TipoMovimiento, TipoMovimientoAdmin)