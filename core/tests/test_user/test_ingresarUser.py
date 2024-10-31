import pytest
from rest_framework.test import APIClient
from authentication.models import CustomUser, Rol 

# H.U. 01: Ingresar al sistema:
@pytest.fixture
def user():
    rol_user, created = Rol.objects.get_or_create(name_role='Usuario')
    return CustomUser.objects.create_user(
        username='juan1', 
        email='juan1@gmail.com', 
        password='admin', 
        is_staff=False, 
        name_role=rol_user
    )

@pytest.mark.django_db
def test_ingresar_al_sistema(user):
    client = APIClient()

    response = client.post('/api/auth/login/', {
        'email': 'juan1@gmail.com',
        'password': 'admin'
    })
    
    assert response.status_code == 200
    assert 'token' in response.data, "El token de autenticación no está"