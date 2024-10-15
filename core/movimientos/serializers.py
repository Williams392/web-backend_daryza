from rest_framework import serializers
from .models import *

# class SucursalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sucursal
#         fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

class DetalleMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleMovimiento
        fields = '__all__'

class TipoMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMovimiento
        fields = '__all__'
