import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse
from gestion_almacen.models import Producto, Marca, Categoria, UnidadMedida
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import CustomUser, Rol
from movimientos.models import TipoMovimiento, Sucursal

from PIL import Image
import io

# # H.U.01: Ingresar Productos al Sistema:
# @pytest.fixture
# def user():
#     rol_user, created = Rol.objects.get_or_create(name_role='Almacen')
#     return CustomUser.objects.create_user(
#         username='williams', 
#         email='williams@gmail.com', 
#         password='admin123456', 
#         is_staff=False, 
#         name_role=rol_user
#     )

# @pytest.fixture
# def crear_categoria():
#     return Categoria.objects.create(nombre_categoria='Limpieza')

# @pytest.fixture
# def crear_marca():
#     return Marca.objects.create(nombre_marca='Daryza')

# @pytest.fixture
# def crear_unidad_medida():
#     return UnidadMedida.objects.create(nombre_unidad='Unidad')

# @pytest.fixture
# def crear_tipo_movimiento():
#     return TipoMovimiento.objects.create(descripcion='Entrada')

# @pytest.fixture
# def crear_sucursal():
#     return Sucursal.objects.create(nombre='Sucursal Lima lurin')

# @pytest.mark.django_db
# def test_ingresar_producto_exito(crear_categoria, crear_marca, crear_unidad_medida, crear_tipo_movimiento, crear_sucursal, user, tmpdir):
#     client = APIClient()
#     token = Token.objects.create(user=user)
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

#     # Debugging: Print user details
#     print(f"Authenticated user: {user.username}, {user.email}")

#     # Create a valid image file using Pillow
#     image_path = tmpdir.join('test_image.jpg')
#     image = Image.new('RGB', (100, 100), color='blue')  # Create a simple blue image
#     image.save(image_path)

#     with open(image_path, 'rb') as img:
#         response = client.post('/api/almacen/productos/', {
#             'nombre_prod': 'Detergente',
#             'descripcion_pro': 'Descripción detergente',
#             'precio_compra': 15.00,
#             'precio_venta': 20.00,
#             'codigo': 'P002',
#             'estado': True,
#             'estock': 200,
#             'estock_minimo': 10,
#             'marca': crear_marca.pk,
#             'categoria': crear_categoria.pk,
#             'unidad_medida': crear_unidad_medida.pk,
#             'tipo_movimiento': crear_tipo_movimiento.pk, 
#             'sucursal': crear_sucursal.pk,  
#             'imagen': SimpleUploadedFile("test_image.jpg", img.read(), content_type="image/jpeg"),
#         })

#         print(response.content)

#         assert response.status_code == 201
#         assert Producto.objects.filter(nombre_prod='Detergente').exists()
#         assert response.data['nombre_prod'] == 'Detergente'
