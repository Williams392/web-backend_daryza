from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Categoria, Marca, UnidadMedida, Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estock', 'marca', 'estado', 'created_at', 'mostrar_imagen')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')


class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviacion')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca)  
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
admin.site.register(Producto, ProductoAdmin)