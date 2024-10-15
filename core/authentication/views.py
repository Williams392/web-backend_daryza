from .serializers import LoginSerializer, UserSerializer, RolSerializer
from .models import CustomUser, Rol
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

from rest_framework.permissions import AllowAny  # Importar AllowAny para permitir el acceso sin autenticación


# Inicio de sesión
class InicioSesionView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

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
            # Aquí se utiliza directamente el campo name_role del usuario autenticado
            name_role = user.name_role

            # Verificar si el usuario tiene el rol de Administrador y asignar superuser
            if name_role and name_role.name_role == "Administrador":
                user.is_superuser = True
                user.save()

            # Generar o recuperar el token para el usuario
            token, _ = Token.objects.get_or_create(user=user)

            user_serializer = UserSerializer(user)
            user_data = dict(user_serializer.data)
            user_data['token'] = str(token.key)  # Añadir el token a los datos del usuario
            
            # Comprobar que name_role es un objeto Rol antes de acceder a sus atributos
            if isinstance(name_role, Rol):
                user_data['role'] = name_role.name_role  # Usar directamente name_role
            else:
                user_data['role'] = None  # O asignar un valor predeterminado

            return Response(user_data, status=status.HTTP_200_OK)
        
        except Rol.DoesNotExist:
            return Response(
                {"code": 301, "msg": "El usuario no tiene un perfil, crea una cuenta primero."},
                status=status.HTTP_301_MOVED_PERMANENTLY
            )


# Registro de nuevos usuarios
class UserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                user = CustomUser.objects.get(pk=pk)
                serializer = self.serializer_class(user)
            except CustomUser.DoesNotExist:
                return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = CustomUser.objects.all()
            serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        last_name = serializer.validated_data['last_name']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        phone_number = serializer.validated_data['phone_number']
        
        # Obtener el rol, si no se proporciona, usar el rol por defecto (1)
        role_id = request.data.get('name_role', 1)

        if not Rol.objects.filter(pk=role_id).exists():
            return Response(
                {
                    "error": "400 Solicitud Incorrecta",
                    "message": f"El rol '{role_id}' no existe.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {
                    "error": "400 Solicitud Incorrecta",
                    "message": f"El correo '{email}' ya está registrado.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(username=username).exists():
            base_username = username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1

        try:
            user = CustomUser(
                username=username,
                email=email,
                phone_number=phone_number,
                last_name=last_name,
                password=make_password(password),
                name_role_id=role_id
            )
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            user_serialized = UserSerializer(user).data
            user_serialized['token'] = str(token.key)
            user_serialized['role'] = role_id

            return Response(user_serialized, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {
                    "error": "400 Solicitud Incorrecta",
                    "message": "Hubo un problema con los datos.",
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


    def put(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Verificar si el correo electrónico ya está en uso por otro usuario
        email = request.data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(pk=pk).exists():
            return Response({"error": "El correo electrónico ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si el nombre de usuario ya está en uso por otro usuario
        username = request.data.get('username')
        if username and CustomUser.objects.filter(username=username).exclude(pk=pk).exists():
            return Response({"error": "El nombre de usuario ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar el rol si se proporciona
        role_id = request.data.get('name_role')
        if role_id:
            if Rol.objects.filter(pk=role_id).exists():
                user.name_role_id = role_id
            else:
                return Response({"error": "El rol no existe."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar los cambios
        serializer.save()
        return Response(serializer.data)


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

# Todo de roles y permisos
class RolListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class RolDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
