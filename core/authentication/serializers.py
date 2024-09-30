from rest_framework import serializers

from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = False, write_only = True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    profile_type = serializers.CharField(required=False, write_only = True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        profile_type = validated_data.pop('profile_type', None)
        user = super().create(validated_data)
        return user, profile_type

    
    # def create(self, validated_data):
    #     print("Creando un usuario")
    #     profile_type = validated_data.pop('profile_type', None)  # Eliminar el campo profile_type si existe
    #     return super().create(validated_data), profile_type



'''
# write_only = true  -> es requerido y cuando el servidor responda con los 
datos del perfil, el campo profile_type no estará presente en la respuesta.

# read_only = true -> n un campo de un serializer indica que el campo solo 
debe ser utilizado para lectura, es decir, para mostrar datos en las respuestas, 
pero no debe ser incluido en las solicitudes para crear o actualizar instancias.
'''
