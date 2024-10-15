# import pytest
# from ..models import Categoria

# @pytest.fixture
# @pytest.mark.django_db
# def categoria():
#     return Categoria.objects.create(
#         nombre='Electronicos',
#         estado=True
#     )

# @pytest.mark.django_db
# def test_crear_categoria(categoria):
#     assert categoria.nombre == 'Electronicos'
#     assert categoria.estado is True
#     assert isinstance(categoria, Categoria)

# @pytest.mark.django_db
# def test_actualizar_categoria(categoria):
#     categoria.nombre = 'Ropa'
#     categoria.save()
#     assert categoria.nombre == 'Ropa'

# @pytest.mark.django_db
# def test_eliminar_categoria(categoria):
#     categoria_id = categoria.id_categoria
#     categoria.delete()
#     with pytest.raises(Categoria.DoesNotExist):
#         Categoria.objects.ge_t(id_categoria=categoria_id)

# @pytest.mark.django_db
# def test_no_crear_categoria_con_nombre_vacio():
#     with pytest.raises(ValueError):
#         Categoria.objects.create(nombre='', estado=True)

# @pytest.mark.django_db
# def test_crear_varias_categorias():
#     Categoria.objects.create(nombre='Juguetes', estado=True)
#     Categoria.objects.create(nombre='Ropa', estado=False)
#     categorias = Categoria.objects.all()
#     assert categorias.count() == 3  
