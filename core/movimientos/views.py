#from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny  # Importar AllowAny para permitir el acceso sin autenticación


class MovimientoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 

    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['fecha', 'tipo_movimiento']

class DetalleMovimientoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 

    queryset = DetalleMovimiento.objects.all()
    serializer_class = DetalleMovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movimiento', 'producto']

class TipoMovimientoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] 

    queryset = TipoMovimiento.objects.all()
    serializer_class = TipoMovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['descripcion']

