from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SucursalViewSet, MovimientoViewSet, DetalleMovimientoViewSet, TipoMovimientoViewSet

router = DefaultRouter()

router.register(r'sucursales', SucursalViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'detallemovimientos', DetalleMovimientoViewSet)
router.register(r'tiposmovimientos', TipoMovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
