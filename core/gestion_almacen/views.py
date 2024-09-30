from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Marca, UnidadMedida, Producto
from .serializers import CategoriaSerializer, MarcaSerializer, UnidadMedidaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'estado']

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'estado']

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'abreviacion']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'codigo', 'estado', 'marca', 'categoria']

# PRODUCTO:

class ProductoFilter(filters.FilterSet):
    nombre = filters.CharFilter(lookup_expr='icontains')  # Filtra por nombre
    marca = filters.CharFilter(field_name='marca__nombre', lookup_expr='icontains')  # Filtra por marca
    categoria = filters.CharFilter(field_name='categoria__nombre', lookup_expr='icontains')  # Filtra por subcategoría

    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'categoria']

class ProductoView(APIView):
    
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

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk_producto=None):
        producto = get_object_or_404(Producto, pk=pk_producto)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_producto=None):
        producto = get_object_or_404(Producto, pk=pk_producto)
        producto.delete()
        return Response({"msg": f"Producto con ID {pk_producto} ha sido eliminado"})
    
