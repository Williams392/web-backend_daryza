import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from authentication.models import CustomUser, Rol 
from gestion_venta.models import Cliente 

# @pytest.fixture
# def admin_user():
#     rol_admin, created = Rol.objects.get_or_create(name_role='Administrador')
    
#     return CustomUser.objects.create_user(
#         username='admin', 
#         email='juan1@gmail.com', 
#         password='admin', 
#         is_staff=True, 
#         name_role=rol_admin
#     )

# # H. U. 05: Actualizar Cliente
# @pytest.fixture
# def cliente_existente():
#     return Cliente.objects.create(
#         nombre_clie='Juan',
#         apellido_clie='Perez',
#         dni_cliente='72345678',
#         ruc_cliente='20999999878',
#         direccion_clie='123 Calle Falsa',
#         razon_socialCliente='empresa alpha s.a.c',
#         tipo_empresa='textil',
#         email_cliente='juan.perez@example.com',
#         telefono_cliente='987654321'
#     )

# @pytest.mark.django_db
# def test_actualizar_cliente(admin_user, cliente_existente):
#     client = APIClient()
#     token = Token.objects.create(user=admin_user)
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
#     response = client.put(f'/api/venta/clientes/{cliente_existente.id_cliente}/', {
#         'nombre_clie': 'Carlos',
#         'apellido_clie': 'Perez',
#         'dni_cliente': '12345678',
#         'ruc_cliente': '20999999878',
#         'direccion_clie': 'carlos.perez@example.com',
#         'razon_socialCliente': 'empresa beta s.a.c',
#         'tipo_empresa': 'textil',
#         'email_cliente': 'carlos.perez@example.com',
#         'telefono_cliente': '987654321'
#     })
#     assert response.status_code == 200
#     cliente_existente.refresh_from_db()
#     assert cliente_existente.nombre_clie == 'Carlos'
#     assert cliente_existente.email_cliente == 'carlos.perez@example.com'