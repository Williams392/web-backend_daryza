import pytest
from gestion_almacen.models import Marca
from django.core.exceptions import ValidationError

@pytest.fixture
def marca():
    return Marca.objects.create(
        nombre_marca='Detergente XYZ',
        estado_marca=True
    )

@pytest.mark.django_db
def test_crear_marca(marca):
    assert marca.nombre_marca == 'Detergente XYZ'
    assert marca.estado_marca is True
    assert isinstance(marca, Marca)

@pytest.mark.django_db
def test_actualizar_marca(marca):
    marca.nombre_marca = 'Limpiador ABC'
    marca.save()
    assert marca.nombre_marca == 'Limpiador ABC'

@pytest.mark.django_db
def test_eliminar_marca(marca):
    marca_id = marca.id_marca
    marca.delete()
    with pytest.raises(Marca.DoesNotExist):
        Marca.objects.get(id_marca=marca_id)

@pytest.mark.django_db
def test_no_crear_marca_con_nombre_vacio():
    marca = Marca(nombre_marca='', estado_marca=True)
    with pytest.raises(ValidationError):
        marca.full_clean()

