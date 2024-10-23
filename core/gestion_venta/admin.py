# gestion_ventas/admin.py

from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(Empresa)
#admin.site.register(Impuesto)
#admin.site.register(EstadoComprobante)
#admin.site.register(TipoComprobante)