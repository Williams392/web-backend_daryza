from rest_framework import serializers
from .models import CustomUser, Rol
from django.contrib.auth.hashers import make_password

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
    password = serializers.CharField(required=False)  # Cambiado a False
    phone_number = serializers.CharField(required=True)
    
    name_role = RolSerializer(read_only=True)
    #name_role = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), write_only=True)


    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': False}  # Asegúrate de que esto esté configurado correctamente
        }

    def get_name_role(self, obj):
        return obj.name_role.name_role if obj.name_role else None

    def create(self, validated_data):
        role_id = validated_data.pop('name_role', None)  # Cambia 'roles' a 'name_role'
        
        # Establece un rol por defecto si no se proporciona uno
        if role_id is None:
            role_id = 1  # Asegúrate de que este ID exista en tu tabla Rol
        
        # Busca el rol por el ID proporcionado
        if not Rol.objects.filter(pk=role_id).exists():
            raise serializers.ValidationError({"error": "El rol no existe."})

        user = CustomUser.objects.create_user(**validated_data, name_role_id=role_id)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        # Actualizar el rol si se proporciona
        role_id = validated_data.get('name_role', None)  # Asegúrate de que este es el ID
        if role_id is not None:
            if Rol.objects.filter(pk=role_id).exists():
                instance.name_role_id = role_id
            else:
                raise serializers.ValidationError({"error": "El rol no existe."})

        # Actualizar la contraseña solo si se proporciona
        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)

        instance.save()
        return instance

