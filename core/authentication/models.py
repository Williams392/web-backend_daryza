from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
# import uuid

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    name_role = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tb_rol'

    def __str__(self):
        return self.name_role
    
class CustomUser(AbstractUser):
    id_user = models.AutoField(primary_key=True)
    #uuid_user = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.EmailField(max_length=150, validators=[EmailValidator()], unique=True, null=True, blank=True)

    phone_number = models.CharField(max_length=15, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name_role = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)

    # campos de django:
    is_staff = models.BooleanField(default=False) 
    #is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False) 
    first_name = models.CharField(max_length=50, null=True, blank=True)  
    last_name = models.CharField(max_length=50, null=True, blank=True)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        db_table = 'tb_usuario'

    def __str__(self):
        return f"{self.username} - {self.email}"
    

    # class Meta:
    #     ordering = ['-id']
