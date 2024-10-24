# gestion_ventas/serializers.py
from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class LegendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legend
        fields = ['id_legend','legend_code', 'legend_value']
        
class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['id_formaPago', 'tipo', 'monto', 'cuota', 'fecha_pago']


class DetalleComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleComprobante
        fields = ['id_detalleComprobante', 'cod_producto', 'unidad', 'descripcion', 'cantidad', 
                  'monto_valorUnitario', 'igv_detalle', 'total_Impuestos',
                  'monto_Precio_Unitario', 'monto_Valor_Venta']


class ComprobanteSerializer(serializers.ModelSerializer):
    detalle = DetalleComprobanteSerializer()
    forma_pago = FormaPagoSerializer()
    legend_comprobante = LegendSerializer()

    class Meta:
        model = Comprobante
        fields = ['uuid_comprobante', 'tipo_operacion', 'tipo_doc', 'numero_serie', 'correlativo',
                  'tipo_moneda', 'fecha_emision', 'empresa_ruc',
                  'cliente_tipo_doc', 'cliente_num_doc', 'cliente_razon_social',
                  'cliente_direccion', 'monto_Oper_Gravadas', 'monto_Igv', 
                  'total_impuestos', 'valor_venta', 'sub_Total',
                  'monto_Imp_Venta', 'estado_Documento', 'manual', 
                  'detalle', 'forma_pago', 'legend_comprobante']

    def validate(self, data):
        # Validar la serie dependiendo del tipo de documento
        if data['tipo_doc'] == "01" and not data['numero_serie'].startswith('F001'):
            raise serializers.ValidationError("La serie para facturas debe comenzar con F001.")
        
        if data['tipo_doc'] == "03" and not data['numero_serie'].startswith('B001'):
            raise serializers.ValidationError("La serie para boletas debe comenzar con B001.")

        # Validar monto máximo para boletas
        if data['tipo_doc'] == "03" and data['monto_Imp_Venta'] > 700.00:
            raise serializers.ValidationError("El monto máximo permitido para una boleta es S/ 700.00.")

        # Validar que el cliente tenga RUC si es una factura
        if data['tipo_doc'] == "01" and data['cliente_tipo_doc'] != "6":  # 6 es el tipo de documento para RUC
            raise serializers.ValidationError("Para facturas, el cliente debe tener RUC.")

        return data

    def create(self, validated_data):
        # Extraer los datos anidados
        detalle_data = validated_data.pop('detalle')
        forma_pago_data = validated_data.pop('forma_pago')
        legend_data = validated_data.pop('legend_comprobante')

        # Crear los objetos anidados
        detalle = DetalleComprobante.objects.create(**detalle_data)
        forma_pago = FormaPago.objects.create(**forma_pago_data)
        legend = Legend.objects.create(**legend_data)

        # Crear el comprobante y vincular los objetos anidados
        comprobante = Comprobante.objects.create(
            **validated_data,
            detalle=detalle,
            forma_pago=forma_pago,
            legend_comprobante=legend
        )

        return comprobante

# class ComprobanteSerializer(serializers.ModelSerializer):
#     # Mantener los serializadores anidados
#     detalle = DetalleComprobanteSerializer(read_only=True)
#     forma_pago = FormaPagoSerializer(read_only=True)
#     legend_comprobante = LegendSerializer(read_only=True)

#     class Meta:
#         model = Comprobante
#         fields = ['uuid_comprobante', 'tipo_operacion', 'tipo_doc', 'numero_serie', 'correlativo',
#                   'tipo_moneda', 'fecha_emision', 'empresa_ruc',
#                   'cliente_tipo_doc', 'cliente_num_doc', 'cliente_razon_social',
#                   'cliente_direccion', 'monto_Oper_Gravadas', 'monto_Igv', 
#                   'total_impuestos', 'valor_venta', 'sub_Total',
#                   'monto_Imp_Venta', 'estado_Documento', 'manual', 
#                   'detalle', 'forma_pago', 'legend_comprobante']

#     # Si quieres serializar desde un objeto con ID y obtener los detalles anidados
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['detalle'] = DetalleComprobanteSerializer(instance.detalle).data
#         representation['forma_pago'] = FormaPagoSerializer(instance.forma_pago).data
#         representation['legend_comprobante'] = LegendSerializer(instance.legend_comprobante).data
#         return representation


        
    # def create(self, validated_data):
    #     # Extrae los datos anidados
    #     detalle_data = validated_data.pop('detalle')
    #     forma_pago_data = validated_data.pop('forma_pago')
    #     legend_comprobante_data = validated_data.pop('legend_comprobante')

    #     # Comprobante sin los campos anidados
    #     comprobante = Comprobante.objects.create(**validated_data)

    #     # los objetos relacionados
    #     DetalleComprobante.objects.create(comprobante=comprobante, **detalle_data)
    #     FormaPago.objects.create(comprobante=comprobante, **forma_pago_data)
    #     Legend.objects.create(comprobante=comprobante, **legend_comprobante_data)

    #     return comprobante


    # def validate(self, data):
    #     tipo_doc = data.get('tipo_doc')
    #     numero_serie = data.get('numero_serie')
    #     cliente_tipo_doc = data.get('cliente_tipo_doc')
    #     monto_Imp_Venta = data.get('monto_Imp_Venta')

    #     if tipo_doc == '01':  # Factura
    #         if not numero_serie.startswith('F'):
    #             raise serializers.ValidationError("La serie de la factura debe comenzar con 'F'.")
    #         if cliente_tipo_doc != '6':
    #             raise serializers.ValidationError("El cliente debe tener RUC para facturas.")
    #     elif tipo_doc == '03':  # Boleta de Venta
    #         if not numero_serie.startswith('B'):
    #             raise serializers.ValidationError("La serie de la boleta debe comenzar con 'B'.")
    #         if monto_Imp_Venta > 700:
    #             raise serializers.ValidationError("El monto máximo para boletas es S/ 700.00.")
    #     else:
    #         raise serializers.ValidationError("Tipo de documento no válido.")

    #     return data

    # def create(self, validated_data):
    #     detalle_data = validated_data.pop('detalle')
    #     forma_pago_data = validated_data.pop('forma_pago')
    #     legend_data = validated_data.pop('legend_comprobante', [])
        
    #     comprobante = Comprobante.objects.create(**validated_data)
        
    #     for item in detalle_data:
    #         DetalleComprobante.objects.create(comprobante=comprobante, **item)
        
    #     for pago in forma_pago_data:
    #         FormaPago.objects.create(comprobante=comprobante, **pago)
        
    #     # Generar automáticamente el legend
    #     total_venta = validated_data['monto_Imp_Venta']
    #     legend_value = f"SON {self.numero_a_letras(total_venta).upper()} CON 00/100 SOLES"
    #     legend_data.append({
    #         'legend_code': '1000',
    #         'legend_value': legend_value
    #     })
        
    #     for legend in legend_data:
    #         Legend.objects.create(comprobante=comprobante, **legend)
        
    #     return comprobante

    # def numero_a_letras(self, numero):
    #     return num2words(numero, lang='es')
