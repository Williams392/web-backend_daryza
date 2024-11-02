import pytest
from django.core.exceptions import ValidationError
from gestion_almacen.models import Categoria

# @pytest.fixture
# def categoria():
#     return Categoria.objects.create(
#         nombre_categoria='Electronicos',
#         estado_categoria=True
#     )

# @pytest.mark.django_db
# def test_crear_categoria(categoria):
#     assert categoria.nombre_categoria == 'Electronicos'
#     assert categoria.estado_categoria is True
#     assert isinstance(categoria, Categoria)

# @pytest.mark.django_db
# def test_actualizar_categoria(categoria):
#     categoria.nombre_categoria = 'Ropa'
#     categoria.save()
#     assert categoria.nombre_categoria == 'Ropa'

# @pytest.mark.django_db
# def test_eliminar_categoria(categoria):
#     categoria_id = categoria.id_categoria
#     categoria.delete()
#     with pytest.raises(Categoria.DoesNotExist):
#         Categoria.objects.get(id_categoria=categoria_id)

# @pytest.mark.django_db
# def test_no_crear_categoria_con_nombre_vacio():
#     categoria = Categoria(nombre_categoria='', estado_categoria=True)
#     with pytest.raises(ValidationError):
#         categoria.full_clean()
