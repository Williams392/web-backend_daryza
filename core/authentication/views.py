from .serializers import LoginSerializer, UserSerializer, RolSerializer, PerfilSerializer
from .models import CustomUser, Rol, Perfil
from rest_framework import generics

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
from authentication.permissions import IsAdmin

# Inicio de sesión
class InicioSesionView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return Response(
                {"code": 400, "msg": "Correo electrónico y contraseña son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password) 
        
        if user is None:
            return Response(
                {"code": 401, "msg": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            perfil = Perfil.objects.get(user=user)
            
            # Verificar si el usuario tiene el rol de Administrador y asignar superuser
            if perfil.name_role.name_role == "Administrador":
                user.is_superuser = True
                user.save()
            
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            user_data = dict(user_serializer.data)
            user_data['token'] = str(token.key)
            return Response(user_data, status=status.HTTP_200_OK)
        
        except Perfil.DoesNotExist:
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
        name_role_id = request.data.get('name_role', None)  # Obtener el rol si está presente

        # Generar un nombre de usuario único
        username = f"{first_name.lower()}_{last_name.lower()}"
        if CustomUser.objects.filter(username=username).exists():
            base_username = username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1

        try:
            # Guardar el usuario
            user = serializer.save(username=username, password=make_password(password))

            # Asociar un rol al perfil solo si se proporciona
            if name_role_id:
                rol = Rol.objects.get(pk=name_role_id)
                perfil = Perfil.objects.create(user=user, name_role=rol)

                # Verificar si el rol es "Administrador" y asignar is_superuser
                if rol.name_role == "Administrador":
                    user.is_superuser = True
                    user.save()

            token, _ = Token.objects.get_or_create(user=user)

            # Serializar los datos de usuario para la respuesta
            user_serialized = UserSerializer(user).data
            user_serialized['token'] = str(token.key)
            user_serialized['role'] = name_role_id

            return Response(user_serialized, status=status.HTTP_201_CREATED)

        except Rol.DoesNotExist:
            return Response(
                {
                    "error": "400 Solicitud Incorrecta",
                    "message": f"El rol '{name_role_id}' no existe.",
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
    #permission_classes = [IsAuthenticated]

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


class RolListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class RolDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

# Vista para CRUD de Perfiles
class PerfilListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

class PerfilDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer