from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):

    class Meta:
        ordering = ['-id']

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=150, unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=False)  # Elimina unique=True si no es necesario
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.username} - {self.email}"

# Modelo de Roles
class Rol(models.Model):
    name_role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name_role
    
class Perfil(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    name_role = models.ForeignKey(Rol, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    