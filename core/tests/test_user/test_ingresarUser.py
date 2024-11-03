# import pytest
# from rest_framework.test import APIClient
# from authentication.models import CustomUser, Rol 

# # H.U. 08: Ingresar al sistema:
# @pytest.fixture
# def user():
#     rol_user, created = Rol.objects.get_or_create(name_role='Usuario')
#     return CustomUser.objects.create_user(
#         username='juan1', 
#         email='juan1@gmail.com', 
#         password='admin123', 
#         is_staff=False, 
#         name_role=rol_user
#     )

# @pytest.mark.django_db
# def test_ingresar_al_sistema(user): # Caso 1
#     client = APIClient()
    
#     # Caso exitoso: Credenciales correctas
#     response = client.post('/api/auth/login/', {
#         'email': 'juan1@gmail.com',
#         'password': 'admin123'
#     })
#     assert response.status_code == 200
#     assert 'token' in response.data, "El token de autenticación no está en la respuesta."

# @pytest.mark.django_db
# def test_ingresar_con_credenciales_invalidas(user): # Caso 2
#     client = APIClient()
    
#     # Error: Credenciales incorrectas
#     response = client.post('/api/auth/login/', {
#         'email': 'adads',
#         'password': 'xxx'
#     })
#     assert response.status_code == 400
#     assert 'msg' in response.data
#     assert response.data['msg'] == "Credenciales inválidas."

