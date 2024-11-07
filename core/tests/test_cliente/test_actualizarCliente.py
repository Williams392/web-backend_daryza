import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from authentication.models import CustomUser, Rol 
from gestion_venta.models import Cliente 

@pytest.fixture
def admin_user():
    rol_admin, created = Rol.objects.get_or_create(name_role='Administrador')
    
    return CustomUser.objects.create_user(
        username='admin', 
        email='juan1@gmail.com', 
        password='admin', 
        is_staff=True, 
        name_role=rol_admin
    )
@pytest.fixture
def cliente():
    return Cliente.objects.create(
        nombre_clie='Juan',
        apellido_clie='Perez',
        dni_cliente='72345678',
        ruc_cliente='20999999878',
        direccion_clie='123 Calle Falsa',
        razon_socialCliente='empresa alpha s.a.c',
        tipo_empresa='textil',
        email_cliente='juan.perez@example.com',
        telefono_cliente='987654321'
    )

@pytest.mark.django_db
def test_actualizar_cliente(admin_user, cliente):
    client = APIClient()
    token = Token.objects.create(user=admin_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = client.put(f'/api/venta/clientes/{cliente.id_cliente}/', {
        'nombre_clie': 'Carlos',
        'apellido_clie': 'Perez',
        'dni_cliente': '12345678',
        'ruc_cliente': '20999999878',
        'direccion_clie': 'carlos.perez@example.com',
        'razon_socialCliente': 'empresa beta s.a.c',
        'tipo_empresa': 'textil',
        'email_cliente': 'carlos.perez@example.com',
        'telefono_cliente': '987654321'
    })
    assert response.status_code == 200
    cliente.refresh_from_db()
    assert cliente.nombre_clie == 'Carlos'
    assert cliente.email_cliente == 'carlos.perez@example.com'

@pytest.mark.django_db
def test_buscar_cliente(admin_user, cliente):
    client = APIClient()
    token = Token.objects.create(user=admin_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    response = client.get(f'/api/venta/clientes/?nombre_clie={cliente.nombre_clie}')
    assert response.status_code == 200
    assert response.data[0]['dni_cliente'] == cliente.dni_cliente

@pytest.mark.django_db
def test_ingresar_nuevo_cliente(admin_user):
    client = APIClient()

    login_success = client.login(email='juan1@gmail.com', password='admin')
    assert login_success, "El login falló"
    
    response = client.post('/api/venta/clientes/', {
        "nombre_clie": "Williams",
        "apellido_clie": "Valle",
        "dni_cliente": "76855212",
        "ruc_cliente": "20999999878",
        "direccion_clie": "av trapiche",
        "razon_socialCliente": "empresa alpha s.a.c",
        "tipo_empresa": "textil",
        "email_cliente": "williams@gmail.com",
        "telefono_cliente": "941412412"
    })
    
    assert response.status_code == 201
    assert Cliente.objects.filter(dni_cliente='76855212').exists()
