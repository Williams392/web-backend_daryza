# gestion_ventas/serializers.py
from rest_framework import serializers
from .models import *
from decimal import Decimal
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast
from .docs.pdf_generator import generar_pdf_comprobante
from django.conf import settings

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'
        
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

    class Meta:
        model = DetalleComprobante
        fields = ['id_detalleComprobante', 'id_producto', 'unidad', 'descripcion', 'cantidad', 
                  'monto_valorUnitario', 'igv_detalle',
                  'monto_Precio_Unitario', 'monto_Valor_Venta']

class ComprobanteSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    sucursal = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all())
    detalle = DetalleComprobanteSerializer(many=True)
    forma_pago = FormaPagoSerializer()
    legend_comprobante = LegendSerializer()

    class Meta:
        model = Comprobante
        fields = [
                'id_comprobante', 'tipo_operacion', 'tipo_doc', 'numero_serie', 'correlativo',
                'tipo_moneda', 'fecha_emision', 'hora_emision',

                'empresa_ruc', 'razon_social', 'nombre_comercial', 'urbanizacion', 
                'distrito', 'departamento', 'email_empresa', 'telefono_emp',

                'cliente_tipo_doc', 'cliente','sucursal',
                'monto_Oper_Gravadas', 'monto_Igv', 
                'valor_venta', 'sub_Total',
                'monto_Imp_Venta', 'estado_Documento', 'manual', 
                'detalle', 'forma_pago', 'legend_comprobante', 
                'usuario', 'pdf_url'
                ]
        extra_kwargs = {
            'monto_Igv': {'required': False},
            #'total_impuestos': {'required': False},
            'correlativo': {'required': False},
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
    
    def get_next_correlativo(self, tipo_doc):
        """
        Obtiene el siguiente número correlativo para el tipo de documento especificado,
        en formato de cinco dígitos con ceros a la izquierda.
        """
        ultimo_comprobante = Comprobante.objects.filter(tipo_doc=tipo_doc).aggregate(
            ultimo_correlativo=Max(Cast('correlativo', output_field=IntegerField()))
        )
        
        # Si es None (no hay registros), iniciar en 1; si no, incrementar
        ultimo_correlativo = ultimo_comprobante['ultimo_correlativo'] or 0
        
        # Incrementar el correlativo y formatearlo a cinco dígitos
        nuevo_correlativo = f"{ultimo_correlativo + 1:05}"
        
        return nuevo_correlativo


    def create(self, validated_data):
        # Extraer los datos anidados
        detalle_data = validated_data.pop('detalle')
        forma_pago_data = validated_data.pop('forma_pago')
        legend_data = validated_data.pop('legend_comprobante')

        # Generar el siguiente correlativo para el tipo de documento
        tipo_doc = validated_data.get('tipo_doc')
        validated_data['correlativo'] = self.get_next_correlativo(tipo_doc)

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

        # Preparar los datos para el PDF, incluyendo datos del cliente y tipo de documento
        cliente = comprobante.cliente  # Cliente relacionado
        comprobante_data = {
            'tipo_doc': comprobante.tipo_doc,
            'numero_serie': comprobante.numero_serie,
            'correlativo': comprobante.correlativo,
            'fecha_emision': comprobante.fecha_emision,
            'razon_social': comprobante.razon_social,
            'urbanizacion': comprobante.urbanizacion,
            'distrito': comprobante.distrito,
            'departamento': comprobante.departamento,
            'email_empresa': comprobante.email_empresa,
            'empresa_ruc': comprobante.empresa_ruc,
            'cliente_tipo_doc': comprobante.cliente_tipo_doc,  # Añadido `cliente_tipo_doc`
            'cliente': {
                'ruc_cliente': cliente.ruc_cliente,
                'razon_socialCliente': cliente.razon_socialCliente,
                'direccion_clie': cliente.direccion_clie,
                'dni_cliente': cliente.dni_cliente,
                'nombre_clie': cliente.nombre_clie,
                'apellido_clie': cliente.apellido_clie,
            }
            # ... otros datos necesarios
        }

        # Generar PDF del comprobante y obtener la ruta de salida
        pdf_path = generar_pdf_comprobante(comprobante_data)

        # Guardar la ruta relativa en `pdf_url`
        pdf_url = pdf_path.replace(settings.MEDIA_ROOT, '')  # Ruta relativa desde MEDIA_ROOT
        comprobante.pdf_url = pdf_url  # Asignar el valor a `pdf_url`
        comprobante.save()  # Guardar los cambios en el comprobante

        return comprobante

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Añadir datos de la sucursal
        sucursal = instance.sucursal
        representation['sucursal'] = {
            'id_sucursal': sucursal.id_sucursal,
            'nombre_sucursal': sucursal.nombre_sucursal,
            'direccion_sucursal': sucursal.direccion_sucursal
        }

        # Añadir datos del cliente
        cliente = instance.cliente
        representation['cliente'] = {
            'id_cliente': cliente.id_cliente,
            'cliente_num_doc': cliente.ruc_cliente,
            'cliente_razon_social': cliente.razon_socialCliente or f"{cliente.nombre_clie} {cliente.apellido_clie}",
            'cliente_direccion': cliente.direccion_clie
        }

        return representation


# class DetalleComprobanteSerializer(serializers.ModelSerializer):

#     monto_valorUnitario = TwoDecimalField(max_digits=10, decimal_places=2)
#     igv_detalle = TwoDecimalField(max_digits=10, decimal_places=2)
#     monto_Precio_Unitario = TwoDecimalField(max_digits=10, decimal_places=2)
#     monto_Valor_Venta = TwoDecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         model = DetalleComprobante
#         fields = ['id_detalleComprobante', 'id_producto', 'unidad', 'descripcion', 'cantidad', 
#                   'monto_valorUnitario', 'igv_detalle',
#                   'monto_Precio_Unitario', 'monto_Valor_Venta']