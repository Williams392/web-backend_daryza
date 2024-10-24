# gestion_ventas/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from num2words import num2words 
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsVentas
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

# Función para convertir el monto a letras en soles
def convertir_a_monto_letras(monto):
    enteros = int(monto)
    decimales = int(round((monto - enteros) * 100))
    
    # Convertir la parte entera del monto a palabras en español
    parte_entera_en_letras = num2words(enteros, lang='es').upper()
    # Crear la representación en letras con los céntimos
    letras = f"SON {parte_entera_en_letras} CON {decimales:02d}/100 SOLES"
    
    return letras

class ComprobanteAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            try:
                comprobante = Comprobante.objects.get(uuid_comprobante=pk)
                serializer = ComprobanteSerializer(comprobante)
                return Response(serializer.data)
            except Comprobante.DoesNotExist:
                return Response({"error": "Comprobante no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            comprobantes = Comprobante.objects.all()
            serializer = ComprobanteSerializer(comprobantes, many=True)
            return Response(serializer.data)

    def post(self, request):
        comprobante_data = request.data

        # Extraer y guardar 'detalle' y 'forma_pago'
        detalle_data = comprobante_data.pop('detalle')
        forma_pago_data = comprobante_data.pop('forma_pago')

        # **Obtener el producto por el id_producto**
        try:
            producto = Producto.objects.get(id_producto=detalle_data['cod_producto'])
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Asignar el nombre_prod como la descripción y la unidad_medida del producto
        detalle_data['descripcion'] = producto.nombre_prod
        detalle_data['unidad'] = producto.unidad_medida.abreviacion  # Unidad del producto
        detalle_data['monto_Precio_Unitario'] = str(producto.precio_venta)  # Precio del producto

        # Calcular monto_Valor_Venta = monto_Precio_Unitario * cantidad
        cantidad = detalle_data.get('cantidad', 1)
        monto_precio_unitario = float(detalle_data['monto_Precio_Unitario'])
        monto_valor_venta = monto_precio_unitario * cantidad

        # Actualizar el monto de valor de venta en el detalle
        detalle_data['monto_Valor_Venta'] = "{:.2f}".format(monto_valor_venta)

        # Calcular el IGV (18%) y total de impuestos
        igv_detalle = monto_valor_venta * 0.18
        detalle_data['igv_detalle'] = "{:.2f}".format(igv_detalle)
        detalle_data['total_Impuestos'] = "{:.2f}".format(igv_detalle)  # Para simplificar, asumimos que solo tiene IGV

        # Serializar los datos del detalle y forma de pago
        detalle_serializer = DetalleComprobanteSerializer(data=detalle_data)
        forma_pago_serializer = FormaPagoSerializer(data=forma_pago_data)

        if detalle_serializer.is_valid() and forma_pago_serializer.is_valid():
            detalle = detalle_serializer.save()
            forma_pago = forma_pago_serializer.save()

            # **Agregar de nuevo el detalle y forma_pago al comprobante_data**
            comprobante_data['detalle'] = detalle_serializer.data
            comprobante_data['forma_pago'] = forma_pago_serializer.data

            # Calcular los totales del comprobante basados en el detalle
            comprobante_data['monto_Oper_Gravadas'] = "{:.2f}".format(monto_valor_venta)  # Valor sin impuestos
            comprobante_data['monto_Igv'] = "{:.2f}".format(igv_detalle)  # IGV
            comprobante_data['total_impuestos'] = "{:.2f}".format(igv_detalle)  # Total de impuestos (solo IGV en este caso)
            comprobante_data['valor_venta'] = "{:.2f}".format(monto_valor_venta)  # Valor de venta sin impuestos
            comprobante_data['sub_Total'] = "{:.2f}".format(monto_valor_venta + igv_detalle)  # Subtotal con impuestos
            comprobante_data['monto_Imp_Venta'] = "{:.2f}".format(monto_valor_venta + igv_detalle)  # Monto total de venta

            # **Generar la leyenda de monto en letras**
            monto_imp_venta = float(comprobante_data['monto_Imp_Venta'])
            legend_value = convertir_a_monto_letras(monto_imp_venta)

            # Crear el legend_comprobante usando el valor generado
            comprobante_data['legend_comprobante'] = {
                "legend_code": "1000",
                "legend_value": legend_value
            }

            # Serializar y guardar el comprobante
            comprobante_serializer = ComprobanteSerializer(data=comprobante_data)
            if comprobante_serializer.is_valid():
                comprobante = comprobante_serializer.save()
                response_serializer = ComprobanteSerializer(comprobante)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            return Response(comprobante_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'detalle_errors': detalle_serializer.errors,
            'forma_pago_errors': forma_pago_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        comprobante = get_object_or_404(Comprobante, pk=pk)
        serializer = ComprobanteSerializer(comprobante, data=request.data, partial=True)
        if serializer.is_valid():
            comprobante = serializer.save()
            return Response(ComprobanteSerializer(comprobante).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comprobante = get_object_or_404(Comprobante, uuid_comprobante=pk)
        comprobante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsVentas]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    
    # Asegúrate de que solo incluyes campos que existen en el modelo Cliente
    filterset_fields = ['nombre_clie', 'apellido_clie']  # Aquí asegúrate que estos existan


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
    filterset_fields = ['ruc_empresa', 'razon_social']  # Asegúrate que estos campos existan en el modelo


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
