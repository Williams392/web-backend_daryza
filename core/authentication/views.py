from .serializers import LoginSerializer, UserSerializer
from .models import ProfileType, Profile

from datetime import datetime

from django.shortcuts import render

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser # porse acaso para la clase registerView


# Inicio de sesión
class InicioSesionView(APIView):

    def post(self, request):
        # Validar que los datos del formulario sean correctos
        email = request.data.get("email")
        password = request.data.get("password")
        
        # 1. Verificar que el email y contraseña sean proporcionados
        if not email or not password:
            return Response(
                {"code": 400, "msg": "Correo electrónico y contraseña son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Limpiar los datos de email
        email = email.strip()

        # 2. Autenticación de usuario
        user = authenticate(request, email=email, password=password) 
        
        if user is None:
            # Credenciales inválidas
            return Response(
                {"code": 401, "msg": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 3. Verificar si el usuario tiene un perfil asociado
        try:
            profile = Profile.objects.get(user=user)
            # Si el usuario tiene un perfil, generar el token y responder con los datos del usuario
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            user_data = dict(user_serializer.data)
            user_data['token'] = str(token.key)
            return Response(user_data, status=status.HTTP_200_OK)
        
        except Profile.DoesNotExist:
            # El usuario no tiene un perfil asociado
            return Response(
                {"code": 301, "msg": "El usuario no tiene un perfil, crea una cuenta primero."},
                status=status.HTTP_301_MOVED_PERMANENTLY
            ) 
        

# Registro de nuevos usuarios
class RegistroView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        username = f"{first_name.lower()}_{last_name.lower()}"
        if CustomUser.objects.filter(username=username).exists():
            base_username = username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1

        try:
            user, profile_type_selected = serializer.save(username=username, password=make_password(password))
            token, _ = Token.objects.get_or_create(user=user)

            if profile_type_selected:
                profile_type = ProfileType.objects.get(pk=profile_type_selected)
                Profile.objects.create(user=user, profile_type=profile_type)

            user_serialized = UserSerializer(user).data
            user_serialized['token'] = str(token.key)
            user_serialized['profile_type'] = profile_type_selected

            return Response(user_serialized, status=status.HTTP_201_CREATED)

        except ProfileType.DoesNotExist:
            return Response(
                {
                    "error": "400 Solicitud Incorrecta",
                    "message": f"El tipo de perfil '{profile_type_selected}' no existe.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "error": "400 Solicitud Incorrecta",
                    "message": f"El correo '{email}' ya está registrado o hubo un problema con los datos.",
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        

# Cierre de sesión de los usuarios autenticados      
class CierreSesionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response(
                {
                    "status": "200 OK",
                    "message": "Has cerrado sesión exitosamente"
                }
            )
        except Token.DoesNotExist:
            return Response(
                {
                    "error": "401 No Autorizado",
                    "message": "Token no asociado al usuario"
                }, status = status.HTTP_401_UNAUTHORIZED
            )
        
# Obtener token oh agregar token a user creado, etc:
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Utiliza 'email' en lugar de 'username' para autenticar
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=400)



# Token Authentication token:
# https://www.django-rest-framework.org/api-guide/authentication/

''''

1. Token: 
se utiliza para generar y almacenar tokens de autenticación para los 
usuarios. Cada token es único y se asocia a un usuario específico.

2. okenAuthentication: 
se utiliza para autenticar las solicitudes basadas en tokens. Esta 
clase verifica que el token proporcionado en la solicitud es válido 
y está asociado a un usuario.

3. IsAuthenticated: 
Es un permiso que se utiliza para restringir el acceso a las vistas 
solo a usuarios autenticados. Si un usuario no está autenticado, no podrá
acceder a las vistas protegidas por este permiso.

'''