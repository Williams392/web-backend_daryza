import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from authentication.models import CustomUser, Rol 
from gestion_venta.models import Cliente 

# # H. U. 03: Ingresar un Nuevo Cliente
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

# @pytest.mark.django_db
# def test_ingresar_nuevo_paciente(admin_user):
#     client = APIClient()

#     login_success = client.login(email='juan1@gmail.com', password='admin')
#     assert login_success, "El login falló"
    
#     response = client.post('/api/venta/clientes/', {
#         "nombre_clie": "Williams",
#         "apellido_clie": "Valle",
#         "dni_cliente": "76855212",
#         "ruc_cliente": "20999999878",
#         "direccion_clie": "av trapiche",
#         "razon_socialCliente": "empresa alpha s.a.c",
#         "tipo_empresa": "textil",
#         "email_cliente": "williams@gmail.com",
#         "telefono_cliente": "941412412"
#     })
    
#     assert response.status_code == 201
#     assert Cliente.objects.filter(dni_cliente='76855212').exists()


