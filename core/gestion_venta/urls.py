# gestion_ventas/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'empresa', EmpresaViewSet)
router.register(r'legend', LegendViewSet)
router.register(r'forma_pago', FormaPagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('', include(router.urls)),

    path('comprobantes/', ComprobanteAPIView.as_view(), name='comprobante-list'),
    path('comprobantes/<int:pk>/', ComprobanteAPIView.as_view(), name='comprobante-detail'),
]
