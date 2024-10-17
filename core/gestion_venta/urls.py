# gestion_ventas/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'comprobantes', ComprobanteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
]
