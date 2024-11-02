from rest_framework import serializers
from .models import CustomUser, Rol
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, 
        validators=[EmailValidator(message="El correo electrónico no tiene un formato válido.")]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=6,
        error_messages={
            'min_length': 'La contraseña debe tener al menos 6 caracteres.'
        }
    )

    def validate(self, data):
        password = data.get('password')
        if password and len(password) < 6:
            raise ValidationError({
                'password': 'La contraseña debe tener al menos 6 caracteres.'
            })
        return data

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_rol', 'name_role']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=False)  # Cambiado a False
    phone_number = serializers.CharField(required=True)
    
    first_name = serializers.CharField(required=False)  # Hacer opcional
    last_name = serializers.CharField(required=False)  # Hacer opcional
    is_staff = serializers.BooleanField(required=False)  # Hacer opcional
    is_active = serializers.BooleanField(required=False)  # Hacer opcional
    is_superuser = serializers.BooleanField(required=False)  # Hacer opcional

    name_role = RolSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': False}  # False significa q el user puede ver su contraseña encriptada. 
        }
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return make_password(value)

    def get_name_role(self, obj):
        return obj.name_role.name_role if obj.name_role else None

    def create(self, validated_data):
        role_id = validated_data.pop('name_role', None)  # Cambia 'roles' a 'name_role'
        
        # Establece un rol por defecto si no se proporciona uno
        if role_id is None:
            role_id = 1  # Asegúrate de que este ID exista en tu tabla Rol

        # Encripta la contraseña antes de crear el usuario
        validated_data['password'] = make_password(validated_data['password'])
        
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

