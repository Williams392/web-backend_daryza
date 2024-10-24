from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'sucursales', SucursalViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'detallemovimientos', DetalleMovimientoViewSet)
router.register(r'tiposmovimientos', TipoMovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('descargar/pdf/', DescargarPDFView.as_view(), name='descargar_pdf'),
    path('descargar/excel/', DescargarExcelView.as_view(), name='descargar_excel'),
]
