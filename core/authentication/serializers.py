from rest_framework import serializers
from .models import CustomUser, Rol

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'name_role']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    
    # Usar el RolSerializer para mostrar el name_role en lugar del ID
    name_role = RolSerializer(read_only=True)  # Se utiliza el serializador de Rol

    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_name_role(self, obj):
        return obj.name_role.name_role if obj.name_role else None

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        user = CustomUser.objects.create_user(**validated_data)
        user.roles.set(roles)
        return user
    
    

