from django.db import models
from django.core.validators import EmailValidator

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    razon_social = models.CharField(max_length=50)  # nombre de la empresa

    tipo_empresa = models.CharField(max_length=50, null=True, blank=False)
    email = models.EmailField(max_length=50, validators=[EmailValidator()], null=True, blank=True)
    telefono_1 = models.CharField(max_length=50, null=True, blank=True)
    telefono_2 = models.CharField(max_length=50, null=True, blank=True)

    # usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
