# gestion_ventas/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsVentas
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *


class ComprobanteAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            comprobante = get_object_or_404(Comprobante, pk=pk)
            serializer = ComprobanteSerializer(comprobante)
        else:
            comprobantes = Comprobante.objects.all()
            serializer = ComprobanteSerializer(comprobantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        comprobante_data = request.data

        # Extraer y guardar 'detalle', 'forma_pago', 'legend_comprobante'
        detalle_data = comprobante_data.pop('detalle')
        forma_pago_data = comprobante_data.pop('forma_pago')
        legend_data = comprobante_data.pop('legend')

        detalle_serializer = DetalleComprobanteSerializer(data=detalle_data)
        forma_pago_serializer = FormaPagoSerializer(data=forma_pago_data)
        legend_serializer = LegendSerializer(data=legend_data)

        if detalle_serializer.is_valid() and forma_pago_serializer.is_valid() and legend_serializer.is_valid():
            detalle = detalle_serializer.save()
            forma_pago = forma_pago_serializer.save()
            legend = legend_serializer.save()

            # Agregar los datos de los objetos guardados al comprobante
            comprobante_data['detalle'] = detalle_serializer.data  # Cambiar a serializer.data
            comprobante_data['forma_pago'] = forma_pago_serializer.data  # Cambiar a serializer.data
            comprobante_data['legend_comprobante'] = legend_serializer.data  # Cambiar a serializer.data

            comprobante_serializer = ComprobanteSerializer(data=comprobante_data)
            if comprobante_serializer.is_valid():
                comprobante = comprobante_serializer.save()
                response_serializer = ComprobanteSerializer(comprobante)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(comprobante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'detalle_errors': detalle_serializer.errors,
            'forma_pago_errors': forma_pago_serializer.errors,
            'legend_errors': legend_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk):
        comprobante = get_object_or_404(Comprobante, pk=pk)
        serializer = ComprobanteSerializer(comprobante, data=request.data, partial=True)
        if serializer.is_valid():
            comprobante = serializer.save()
            return Response(ComprobanteSerializer(comprobante).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comprobante = get_object_or_404(Comprobante, pk=pk)
        comprobante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_clie', 'apellido_clie', 'razon_socialCliente']

class FormaPagoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'monto']

class LegendViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Legend.objects.all()
    serializer_class = LegendSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['legend_code', 'comprobante']

class EmpresaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ruc_empresa', 'razon_social']

# class EstadoComprobanteViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsVentas]
#     queryset = EstadoComprobante.objects.all()
#     serializer_class = EstadoComprobanteSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['nombre_estado']

# class TipoComprobanteViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsVentas]
#     queryset = TipoComprobante.objects.all()
#     serializer_class = TipoComprobanteSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['nombre_tipo']

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