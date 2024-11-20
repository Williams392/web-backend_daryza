from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'productos', DashboardViewProductoSet, basename='dashboard-productos') 
router.register(r'clientes', DashboardViewClienteSet, basename='dashboard-clientes') 
router.register(r'comprobantes', DashboardViewComprobanteSet, basename='dashboard-comprobantes') 
router.register(r'usuarios', DashboardViewUsuarioSet, basename='dashboard-usuarios')
router.register(r'movimientos', DashboardVieMovieminentoSet, basename='dashboard-movimiento')

urlpatterns = [

    path('', include(router.urls)),

] 
