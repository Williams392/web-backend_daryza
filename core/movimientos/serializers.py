from rest_framework import serializers
from .models import *

# class SucursalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sucursal
#         fields = '__all__'

# class MovimientoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movimiento
#         fields = '__all__'

class TipoMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMovimiento
        fields = '__all__'

class DetalleMovimientoSerializer(serializers.ModelSerializer):
    # Incluir el nombre del producto relacionado
    nombre_prod = serializers.CharField(source='producto.nombre_prod', read_only=True)

    class Meta:
        model = DetalleMovimiento
        fields = ['id_detalleMovimiento', 'cantidad', 'nombre_prod', 'movimiento', 'detalleComprobante']

class MovimientoSerializer(serializers.ModelSerializer):
    detalles = DetalleMovimientoSerializer(source='detallemovimiento_set', many=True, read_only=True)

    class Meta:
        model = Movimiento
        fields = ['id_movimiento', 'referencia', 'cant_total', 'created_at', 'updated_at', 'sucursal', 'usuario', 'tipo_movimiento', 'detalles']
