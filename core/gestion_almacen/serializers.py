from rest_framework import serializers
from .models import Categoria, Marca, UnidadMedida, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

    def validate(self, data):
        instance = self.instance

        if instance and instance.nombre_categoria != data['nombre_categoria']:
            if Categoria.objects.filter(nombre_categoria=data['nombre_categoria']).exists():
                raise serializers.ValidationError({"nombre_categoria": "El nombre de la categoría ya existe."})

        return data


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

    def validate(self, data):
        instance = self.instance

        if instance and instance.nombre_marca != data['nombre_marca']:
            if Marca.objects.filter(nombre_marca=data['nombre_marca']).exists():
                raise serializers.ValidationError({"nombre_marca": "El nombre de la marca ya existe."})

        return data


class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

    def validate(self, data):
        # Obtener la instancia actual si existe
        instance = self.instance

        # Validar nombre_unidad solo si ha cambiado
        if instance and instance.nombre_unidad != data['nombre_unidad']:
            if UnidadMedida.objects.filter(nombre_unidad=data['nombre_unidad']).exists():
                raise serializers.ValidationError({"nombre_unidad": "El nombre de la Unidad Medida ya existe."})

        # Validar abreviacion solo si ha cambiado
        if instance and instance.abreviacion != data['abreviacion']:
            if UnidadMedida.objects.filter(abreviacion=data['abreviacion']).exists():
                raise serializers.ValidationError({"abreviacion": "La abreviación de la Unidad Medida ya existe."})

        return data

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        extra_kwargs = {
            'codigo': {'required': False}
        }

    def validate(self, data):
        if data['precio_venta'] <= data['precio_compra']: 
            raise serializers.ValidationError("El precio de compra debe ser mayor que el precio de venta.")
        if data['estock'] <= data['estock_minimo']:
            raise serializers.ValidationError("El estock debe ser mayor que el estock mínimo y no pueden ser iguales.")
        return data
    
    def create(self, validated_data):
        producto = Producto.objects.create(**validated_data)
        producto.codigo = f'P-{producto.id_producto:09d}'
        producto.save()
        return producto

    def update(self, instance, validated_data):
        # Manejo especial para el archivo de imagen, si es proporcionado
        imagen = validated_data.pop('imagen', None)
        if imagen:
            instance.imagen = imagen
        
        return super().update(instance, validated_data)
