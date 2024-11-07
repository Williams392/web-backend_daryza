# import pytest
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APIClient
# from authentication.models import CustomUser, Rol 
# from gestion_venta.models import Cliente 

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

# # H. U. 04: Buscar Cliente
# @pytest.fixture
# def cliente():
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
# def test_buscar_paciente(admin_user, cliente):
#     client = APIClient()
#     token = Token.objects.create(user=admin_user)
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
#     response = client.get(f'/api/venta/clientes/?nombre_clie={cliente.nombre_clie}')
#     assert response.status_code == 200
#     assert response.data[0]['dni_cliente'] == cliente.dni_cliente
