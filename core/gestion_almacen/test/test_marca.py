# import pytest
# from ..models import Marca

# @pytest.fixture
# @pytest.mark.django_db
# def marca():
#     return Marca.objects.create(
#         nombre='Detergente XYZ',
#         estado=True
#     )

# @pytest.mark.django_db
# def test_crear_marca(marca):
#     assert marca.nombre == 'Detergente XYZ'
#     assert marca.estado is True
#     assert isinstance(marca, Marca)

# @pytest.mark.django_db
# def test_actualizar_marca(marca):
#     marca.nombre = 'Limpiador ABC'
#     marca.save()
#     assert marca.nombre == 'Limpiador ABC'

# @pytest.mark.django_db
# def test_eliminar_marca(marca):
#     marca_id = marca.id_marca
#     marca.delete()
#     with pytest.raises(Marca.DoesNotExist):
#         Marca.objects.get(id_marca=marca_id)

# @pytest.mark.django_db
# def test_no_crear_marca_con_nombre_vacio():
#     with pytest.raises(ValueError):
#         Marca.objects.create(nombre='', estado=True)

# @pytest.mark.django_db
# def test_crear_varias_marcas():
#     Marca.objects.create(nombre='Desinfectante 123', estado=True)
#     Marca.objects.create(nombre='Limpiador Multiusos', estado=False)
#     marcas = Marca.objects.all()
#     assert marcas.count() == 3  

