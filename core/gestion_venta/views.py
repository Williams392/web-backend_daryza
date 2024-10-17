# gestion_ventas/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsVentas
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_clie', 'apellido_clie', 'razon_socialCliente']

class ComprobanteViewSet(viewsets.ModelViewSet):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        comprobante = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(comprobante)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            comprobante = serializer.save()
            return Response(ComprobanteSerializer(comprobante).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        comprobante = self.get_object()
        serializer = self.get_serializer(comprobante, data=request.data, partial=True)
        if serializer.is_valid():
            comprobante = serializer.save()
            return Response(ComprobanteSerializer(comprobante).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        comprobante = self.get_object()
        comprobante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)