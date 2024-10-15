# gestion_ventas/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsVentas
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Emisor.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'apellido', 'razon_social']
