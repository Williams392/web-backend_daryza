import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUser, Rol

#H. U. 12: Registro de un Nuevo Usuario
@pytest.fixture
def rol_usuario():
    return Rol.objects.create(name_role='Administrador')

@pytest.mark.django_db
def test_registrar_nuevo_usuario_exito(rol_usuario):
    client = APIClient()
    response = client.post('/api/auth/signup/', {
        'username': 'Jords2',
        'last_name': 'Flores',
        'email': 'jords@gmail.com',
        'password': 'Admin1234!',
        'phone_number': '+51994469322',
        'name_role': rol_usuario.pk
    })
    assert response.status_code == 201
    assert CustomUser.objects.filter(username='Jords2').exists()

@pytest.mark.django_db
def test_registrar_usuario_email_existente(rol_usuario):
    CustomUser.objects.create(username='Jords2', email='jords@gmail.com', password='admin123456', phone_number='+51994469322')
    client = APIClient()
    response = client.post('/api/auth/signup/', {
        'username': 'NewUser',
        'last_name': 'NewLastName',
        'email': 'jords@gmail.com',
        'password': 'Admin1234!',
        'phone_number': '+51994469323',
        'name_role': rol_usuario.pk
    })
    assert response.status_code == 400
    assert 'correo' in response.data.get('message', '').lower()

@pytest.mark.django_db
def test_registrar_usuario_password_debil(rol_usuario):
    client = APIClient()
    response = client.post('/api/auth/signup/', {
        'username': 'Jords3',
        'last_name': 'Flores',
        'email': 'jords3@gmail.com',
        'password': '1234',
        'phone_number': '+51994469322',
        'name_role': rol_usuario.pk
    })
    assert response.status_code == 400
    assert 'contraseña' in response.data.get('message', '').lower()
