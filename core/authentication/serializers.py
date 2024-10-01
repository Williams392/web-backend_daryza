from rest_framework import serializers
from .models import CustomUser, Rol, Perfil

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    roles = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), many=True, required=False)  # Hacer roles opcional

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        user = super().create(validated_data)
        if roles:
            user.roles.set(roles)  # Asignar roles solo si existen
        return user

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'name_role']

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'user', 'name_role']
        depth = 1  # Para mostrar detalles del usuario y rol