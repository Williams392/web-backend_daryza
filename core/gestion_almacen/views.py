from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Marca, UnidadMedida, Producto
from .serializers import CategoriaSerializer, MarcaSerializer, UnidadMedidaSerializer, ProductoSerializer

from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAlmacen
from movimientos.models import Movimiento, DetalleMovimiento, TipoMovimiento
from gestion_venta.models import DetalleComprobante
from django.db import transaction
from django.utils import timezone
import uuid 
from django.db.models.signals import post_save
import re 

class ProductoFilter(filters.FilterSet):
    nombre_prod = filters.CharFilter(lookup_expr='icontains') 
    marca = filters.CharFilter(field_name='marca__nombre', lookup_expr='icontains')  
    categoria = filters.CharFilter(field_name='categoria__nombre', lookup_expr='icontains') 

    class Meta:
        model = Producto
        fields = ['nombre_prod', 'codigo', 'marca', 'categoria']

# CRUD:
class ProductoView(APIView):
    permission_classes = [IsAuthenticated, IsAlmacen]
    # quite el permiso para el user ventas puede aceder a producto.
    
    def get(self, request, pk_producto=None):
        if pk_producto:  # Ver detalles de un producto específico
            producto = get_object_or_404(Producto, pk=pk_producto)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data)
        else:  # Ver todos los productos
            queryset = Producto.objects.all()
            # Aplica filtros manualmente
            filtro = ProductoFilter(request.GET, queryset=queryset)
            productos = filtro.qs  # Obtiene los productos filtrados
            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        
        if serializer.is_valid():
            producto = serializer.save()

            tipo_movimiento = TipoMovimiento.objects.get(descripcion='Entrada')
            movimiento = Movimiento.objects.create(
                referencia='Ingreso de productos',
                cant_total=producto.estock,
                sucursal_id=1,
                usuario=request.user,
                tipo_movimiento=tipo_movimiento,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            DetalleMovimiento.objects.create(
                cantidad=producto.estock,
                producto=producto,
                movimiento=movimiento
            )

            post_save.send(sender=Producto, instance=producto, created=True, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @transaction.atomic
    def put(self, request, pk_producto=None):
        producto = get_object_or_404(Producto, pk=pk_producto)
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def delete(self, request, pk_producto=None):
        producto = get_object_or_404(Producto, pk=pk_producto)
        producto.delete(usuario=request.user)
        return Response({"msg": f"Producto con ID {pk_producto} ha sido eliminado"})


class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAlmacen]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_categoria', 'estado_categoria']

class MarcaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAlmacen]
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_marca', 'estado_marca']

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAlmacen]
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_unidad', 'abreviacion']