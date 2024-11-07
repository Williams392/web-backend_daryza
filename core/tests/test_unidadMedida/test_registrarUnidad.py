# import pytest
# from gestion_almacen.models import UnidadMedida
# from django.core.exceptions import ValidationError

# @pytest.fixture
# def unidad_medida():
#     return UnidadMedida.objects.create(
#         nombre_unidad='Kilogramo',
#         abreviacion='kg'
#     )

# @pytest.mark.django_db
# def test_crear_unidad_medida(unidad_medida):
#     assert unidad_medida.nombre_unidad == 'Kilogramo'
#     assert unidad_medida.abreviacion == 'kg'
#     assert isinstance(unidad_medida, UnidadMedida)

# @pytest.mark.django_db
# def test_actualizar_unidad_medida(unidad_medida):
#     unidad_medida.nombre_unidad = 'Litro'
#     unidad_medida.abreviacion = 'L'
#     unidad_medida.save()
#     assert unidad_medida.nombre_unidad == 'Litro'
#     assert unidad_medida.abreviacion == 'L'

# @pytest.mark.django_db
# def test_eliminar_unidad_medida(unidad_medida):
#     unidad_medida_id = unidad_medida.id_unidadMedida
#     unidad_medida.delete()
#     with pytest.raises(UnidadMedida.DoesNotExist):
#         UnidadMedida.objects.get(id_unidadMedida=unidad_medida_id)

# @pytest.mark.django_db
# def test_no_crear_unidad_medida_con_nombre_duplicado():
#     UnidadMedida.objects.create(nombre_unidad='Metro', abreviacion='m')
#     with pytest.raises(ValidationError):
#         unidad_medida_duplicada = UnidadMedida(nombre_unidad='Metro', abreviacion='m2')
#         unidad_medida_duplicada.full_clean()

# @pytest.mark.django_db
# def test_no_crear_unidad_medida_con_abreviacion_duplicada():
#     UnidadMedida.objects.create(nombre_unidad='Gramo', abreviacion='g')
#     with pytest.raises(ValidationError):
#         unidad_medida_duplicada = UnidadMedida(nombre_unidad='Mililitro', abreviacion='g')
#         unidad_medida_duplicada.full_clean()
