from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from reports.reporte_movimientos import DescargarMovimientoPDFView, DescargarExcelMovimientoView

router = DefaultRouter()
router.register(r'auditorias', AuditoriaViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'detallemovimientos', DetalleMovimientoViewSet)
router.register(r'tiposmovimientos', TipoMovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('descargar/pdf/', DescargarMovimientoPDFView.as_view(), name='descargar_pdf'),
    path('descargar/excel/', DescargarExcelMovimientoView.as_view(), name='descargar_excel'),
]
