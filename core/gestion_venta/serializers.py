# gestion_ventas/serializers.py
from rest_framework import serializers
from .models import *
from decimal import Decimal

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'nombre_clie', 'apellido_clie', 
                  'dni_cliente', 'ruc_cliente','direccion_clie', 'razon_socialCliente',
                  'tipo_empresa', 'email_cliente', 'telefono_cliente']

    def validate(self, data):
        instance = self.instance

        # Validar dni_cliente
        if 'dni_cliente' in data:
            dni_cliente = data['dni_cliente']
            if Cliente.objects.filter(dni_cliente=dni_cliente).exclude(id_cliente=instance.id_cliente if instance else None).exists():
                raise serializers.ValidationError({"dni_cliente": "El DNI del cliente ya existe."})

        # Validar ruc_cliente
        if 'ruc_cliente' in data:
            ruc_cliente = data['ruc_cliente']
            if Cliente.objects.filter(ruc_cliente=ruc_cliente).exclude(id_cliente=instance.id_cliente if instance else None).exists():
                raise serializers.ValidationError({"ruc_cliente": "El RUC del cliente ya existe."})

        return data

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

class TwoDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        if value is None:
            return value
        return float(Decimal(value).quantize(Decimal('0.00')))
    
class DetalleComprobanteSerializer(serializers.ModelSerializer):

    monto_valorUnitario = TwoDecimalField(max_digits=10, decimal_places=2)
    igv_detalle = TwoDecimalField(max_digits=10, decimal_places=2)
    total_Impuestos = TwoDecimalField(max_digits=10, decimal_places=2)
    monto_Precio_Unitario = TwoDecimalField(max_digits=10, decimal_places=2)
    monto_Valor_Venta = TwoDecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = DetalleComprobante
        fields = ['id_detalleComprobante', 'cod_producto', 'unidad', 'descripcion', 'cantidad', 
                  'monto_valorUnitario', 'igv_detalle', 'total_Impuestos',
                  'monto_Precio_Unitario', 'monto_Valor_Venta']

class ComprobanteSerializer(serializers.ModelSerializer):
    detalle = DetalleComprobanteSerializer(many=True)
    forma_pago = FormaPagoSerializer()
    legend_comprobante = LegendSerializer()

    monto_Oper_Gravadas = TwoDecimalField(max_digits=10, decimal_places=2)
    monto_Igv = TwoDecimalField(max_digits=10, decimal_places=2)
    total_impuestos = TwoDecimalField(max_digits=10, decimal_places=2)
    valor_venta = TwoDecimalField(max_digits=10, decimal_places=2)
    sub_Total = TwoDecimalField(max_digits=10, decimal_places=2)
    monto_Imp_Venta = TwoDecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Comprobante
        fields = ['uuid_comprobante', 'tipo_operacion', 'tipo_doc', 'numero_serie', 'correlativo',
                  'tipo_moneda', 'fecha_emision', 'empresa_ruc',
                  'cliente_tipo_doc', 'cliente_num_doc', 'cliente_razon_social',
                  'cliente_direccion', 'monto_Oper_Gravadas', 'monto_Igv', 
                  'total_impuestos', 'valor_venta', 'sub_Total',
                  'monto_Imp_Venta', 'estado_Documento', 'manual', 
                  'detalle', 'forma_pago', 'legend_comprobante']
        extra_kwargs = {
            'monto_Igv': {'required': False},
            'total_impuestos': {'required': False},
            'sub_Total': {'required': False},
            'monto_Imp_Venta': {'required': False},
        }

    def validate(self, data):
        # Validar la serie dependiendo del tipo de documento
        if data['tipo_doc'] == "01" and not data['numero_serie'].startswith('F001'):
            raise serializers.ValidationError("La serie para facturas debe comenzar con F001.")
        
        if data['tipo_doc'] == "03" and not data['numero_serie'].startswith('B001'):
            raise serializers.ValidationError("La serie para boletas debe comenzar con B001.")

        if data['tipo_doc'] == "03" and data['monto_Imp_Venta'] > 700.00:
            raise serializers.ValidationError("El monto máximo permitido para una boleta es S/ 700.00.")

        if data['tipo_doc'] == "01" and data['cliente_tipo_doc'] != "6":  # 6 es el tipo de documento para RUC
            raise serializers.ValidationError("Para facturas, el cliente debe tener RUC.")

        return data

    def create(self, validated_data):
        # Extraer los datos anidados
        detalle_data = validated_data.pop('detalle')
        forma_pago_data = validated_data.pop('forma_pago')
        legend_data = validated_data.pop('legend_comprobante')

        # Crear los objetos anidados
        forma_pago = FormaPago.objects.create(**forma_pago_data)
        legend = Legend.objects.create(**legend_data)

        # Crear el comprobante sin los detalles primero
        comprobante = Comprobante.objects.create(
            **validated_data,
            forma_pago=forma_pago,
            legend_comprobante=legend
        )

        # Crear los detalles y asignarles el comprobante creado
        for detalle in detalle_data:
            DetalleComprobante.objects.create(comprobante=comprobante, **detalle)

        return comprobante
