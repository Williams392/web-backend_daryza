from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Categoria, Marca, UnidadMedida, Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_prod', 'estock', 'marca', 'estado', 'created_at', 'mostrar_imagen')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria', 'estado')


class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre_unidad', 'abreviacion')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca)  
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
admin.site.register(Producto, ProductoAdmin)