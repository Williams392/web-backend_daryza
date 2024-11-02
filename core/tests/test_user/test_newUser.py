import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUser, Rol 


# H. U. 02: Registrar un Nuevo Usuario
# @pytest.fixture
# def rol_usuario():
#     return Rol.objects.create(name_role='Administrador')

# @pytest.mark.django_db
# def test_registrar_nuevo_usuario(rol_usuario):
#     client = APIClient()
    
#     response = client.post('/api/auth/signup/', {
#         'username': 'Jords2',
#         'last_name': 'Flores',
#         'email': 'jords@gmail.com',
#         'password': 'admin123456',
#         'phone_number': '+51994469322',
#         'name_role': rol_usuario.pk 
#     })
#     if response.status_code != 201:
#         print(response.data) 
#     assert response.status_code == 201
#     assert CustomUser.objects.filter(username='Jords2').exists()