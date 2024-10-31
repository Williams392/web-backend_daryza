# gestion_ventas/admin.py

from django.contrib import admin
from .models import *

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombre_clie', 'dni_cliente', 'ruc_cliente')

class LegendAdmin(admin.ModelAdmin):
    list_display = ('id_legend', 'legend_value')

class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ('id_formaPago', 'monto', 'fecha_emision', 'fecha_vencimiento')

class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('id_comprobante', 'tipo_operacion', 'numero_serie', 'fecha_emision', 'hora_emision')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Legend, LegendAdmin)  
admin.site.register(FormaPago, FormaPagoAdmin)
admin.site.register(Comprobante, ComprobanteAdmin)

