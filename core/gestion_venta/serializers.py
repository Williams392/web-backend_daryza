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
        extra_kwargs = {
            'dni_cliente': {'required': False},
            'ruc_cliente': {'required': True}
        }

    def validate(self, data):
        instance = self.instance

        if 'dni_cliente' in data:   # Validar dni_cliente
            dni_cliente = data['dni_cliente']
            if Cliente.objects.filter(dni_cliente=dni_cliente).exclude(id_cliente=instance.id_cliente if instance else None).exists():
                raise serializers.ValidationError({"dni_cliente": "El DNI del cliente ya existe."})

        if 'ruc_cliente' in data: # Validar ruc_cliente
            ruc_cliente = data['ruc_cliente']
            if Cliente.objects.filter(ruc_cliente=ruc_cliente).exclude(id_cliente=instance.id_cliente if instance else None).exists():
                raise serializers.ValidationError({"ruc_cliente": "El RUC del cliente ya existe."})

        return data

# class EmpresaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Empresa
#         fields = '__all__'

class LegendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legend
        fields = ['id_legend','legend_code', 'legend_value']
        
class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = ['id_formaPago', 'tipo', 'monto', 'cuota', 'fecha_emision', 'fecha_vencimiento']

class TwoDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        if value is None:
            return value
        return Decimal(value).quantize(Decimal('0.00'))
    
class DetalleComprobanteSerializer(serializers.ModelSerializer):

    monto_valorUnitario = TwoDecimalField(max_digits=10, decimal_places=2)
    igv_detalle = TwoDecimalField(max_digits=10, decimal_places=2)
    #total_Impuestos = TwoDecimalField(max_digits=10, decimal_places=2)
    monto_Precio_Unitario = TwoDecimalField(max_digits=10, decimal_places=2)
    monto_Valor_Venta = TwoDecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = DetalleComprobante
        fields = ['id_detalleComprobante', 'id_producto', 'unidad', 'descripcion', 'cantidad', 
                  'monto_valorUnitario', 'igv_detalle',
                  'monto_Precio_Unitario', 'monto_Valor_Venta']

class ComprobanteSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    detalle = DetalleComprobanteSerializer(many=True)
    forma_pago = FormaPagoSerializer()
    legend_comprobante = LegendSerializer()

    class Meta:
        model = Comprobante
        fields = ['uuid_comprobante', 'tipo_operacion', 'tipo_doc', 'numero_serie', 'correlativo',
                  'tipo_moneda', 'fecha_emision', 

                  'empresa_ruc', 'razon_social', 'nombre_comercial', 'urbanizacion', 
                  'distrito', 'departamento', 'email_empresa', 'telefono_emp',

                  'cliente_tipo_doc', 'cliente',
                  'monto_Oper_Gravadas', 'monto_Igv', 
                  'valor_venta', 'sub_Total',
                  'monto_Imp_Venta', 'estado_Documento', 'manual', 
                  'detalle', 'forma_pago', 'legend_comprobante']
        extra_kwargs = {
            'monto_Igv': {'required': False},
            #'total_impuestos': {'required': False},
            'sub_Total': {'required': False},
            'monto_Imp_Venta': {'required': False},
            'email_empresa': {'required': False},
            'telefono_emp': {'required': False},
        }

    def validate(self, data):
        
        # Validación para Facturas (tipo_doc "01")
        if data['tipo_doc'] == "01":  # Factura
            if not data['numero_serie'].startswith('F001'):
                raise serializers.ValidationError("La serie para facturas debe comenzar con F001.")
            if data['cliente_tipo_doc'] != "6":  # 6 = RUC
                raise serializers.ValidationError("Para facturas, el cliente debe tener RUC (tipo de documento '6').")

        # Validación para Boletas (tipo_doc "03")
        elif data['tipo_doc'] == "03":  # Boleta
            if not data['numero_serie'].startswith('B001'):
                raise serializers.ValidationError("La serie para boletas debe comenzar con B001.")
            if data['cliente_tipo_doc'] not in ["1", "6"]:  # 1 = DNI, 6 = RUC
                raise serializers.ValidationError("Para boletas, el cliente debe tener DNI (tipo '1') o RUC (tipo '6').")
            if data['monto_Imp_Venta'] > 700.00:
                raise serializers.ValidationError("El monto máximo permitido para una boleta es S/ 700.00.")

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cliente = instance.cliente  # Obtener el cliente relacionado
        
        # Simplificar representación del cliente, sin lógica para cliente_num_doc
        representation['cliente'] = {
            'cliente_id': cliente.id_cliente,
            'cliente_num_doc': cliente.ruc_cliente, 
            'cliente_razon_social': cliente.razon_socialCliente or f"{cliente.nombre_clie} {cliente.apellido_clie}",
            'cliente_direccion': cliente.direccion_clie
        }
        return representation

