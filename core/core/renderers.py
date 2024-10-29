# mi_app/renderers.py
from rest_framework.renderers import JSONRenderer
from decimal import Decimal

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            data = self.format_decimals(data)
        return super().render(data, accepted_media_type, renderer_context)

    def format_decimals(self, data):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value.quantize(Decimal('0.00')))
            elif isinstance(value, list):
                data[key] = [self.format_decimals(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                data[key] = self.format_decimals(value)
        return data
