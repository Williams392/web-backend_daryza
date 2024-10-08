from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Rol(models.Model):
    name_role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name_role
    
class CustomUser(AbstractUser):

    class Meta:
        ordering = ['-id']

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=150, unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name_role = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.username} - {self.email}"
