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

    USERNAME_FIELD = 'email' # cambiando el login de admin a email:
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.username} - {self.email}"

# Tipo de Perfil:
class ProfileType(models.Model):
    #id_tipoPerfil = models.AutoField(max_length=50, primary_key=True)
    profile_type = models.CharField(max_length = 50)

    """
    Catálogo para manejar los tipos de perfiles:
    1. Administrador
    2. Almacenero
    3. Cajero
    """

    def __str__(self):
        return self.profile_type

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    


'''
    Class profile:

    No es bueno poner todos estos datos, esta clase es para 
    la eleccion que tipo de perfil, no es crear un user.
    
    biography = models.TextField(blank=True) 
    company = models.CharField(max_length=70, blank=True)
    address = models.CharField(max_length=200, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=250, blank=True)
    linkedin_link = models.URLField(max_length=250, blank=True)
    website_link = models.URLField(max_length=250, blank=True)
    birthday = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
'''