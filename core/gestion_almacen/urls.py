from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoView, CategoriaViewSet, MarcaViewSet, UnidadMedidaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'unidadesmedida', UnidadMedidaViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('productos/', ProductoView.as_view(), name='producto-list'),  # Listar y crear productos
    path('productos/<int:pk_producto>/', ProductoView.as_view(), name='producto-detail'),  # Detalles, actualizar y eliminar un producto
] 
