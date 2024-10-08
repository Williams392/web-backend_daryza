from rest_framework import serializers
from .models import Categoria, Marca, UnidadMedida, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate(self, data):
        print("Validando datos:", data)  # Imprimir los datos que se están validando

        if data['precio_venta'] <= data['precio_compra']: 
            print("Error: El precio de compra debe ser mayor que el precio de venta.")
            raise serializers.ValidationError("El precio de compra debe ser mayor que el precio de venta.")

        if data['estock'] <= data['estock_minimo']:
            print("Error: El estock debe ser mayor que el estock mínimo y no pueden ser iguales.")
            raise serializers.ValidationError("El estock debe ser mayor que el estock mínimo y no pueden ser iguales.")
            
        return data
