# gestion_ventas/urls.py

from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'legend', LegendViewSet)
router.register(r'forma_pago', FormaPagoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comprobantes/', ComprobanteAPIView.as_view(), name='comprobante-list'),
    path('comprobantes/<str:pk>/', ComprobanteAPIView.as_view(), name='comprobante-detail'),
    path('comprobantes/pdf/<str:pk>/', ComprobantePDFView.as_view(), name='comprobante-pdf'),
]
