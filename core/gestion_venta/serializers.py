# gestion_ventas/serializers.py
from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DetalleComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleComprobante
        fields = ['unidad', 'cantidad', 'cod_producto', 'descripcion', 
                  'mto_valorUnitario', 'mto_valorTotal', 'igv_detalle']

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['tipo', 'monto', 'cuota', 'fecha_pago']

class LegendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legend
        fields = ['legend_code', 'legend_value']

class ComprobanteSerializer(serializers.ModelSerializer):
    detalle = DetalleComprobanteSerializer(many=True)
    forma_pago = FormaPagoSerializer(many=True)
    legend = LegendSerializer(many=True)

    class Meta:
        model = Comprobante
        fields = ['tipo_operacion', 'tipo_doc', 'numero_serie', 'correlativo',
                  'tipo_moneda', 'fecha_emision', 'hora_emision', 'empresa_ruc',
                  'cliente_tipo_doc', 'cliente_num_doc', 'cliente_razon_social',
                  'cliente_direccion', 'mto_operGravadas', 'mto_igv', 
                  'total_impuestos', 'valor_venta', 'sub_totalVenta',
                  'mto_importeTotal', 'detalle', 'forma_pago', 'legend']

    def create(self, validated_data):
        detalle_data = validated_data.pop('detalle')
        forma_pago_data = validated_data.pop('forma_pago')
        legend_data = validated_data.pop('legend')

        comprobante = Comprobante.objects.create(**validated_data)

        for item in detalle_data:
            DetalleComprobante.objects.create(comprobante=comprobante, **item)

        for pago in forma_pago_data:
            FormaPago.objects.create(comprobante=comprobante, **pago)

        for legend in legend_data:
            Legend.objects.create(comprobante=comprobante, **legend)

        return comprobante