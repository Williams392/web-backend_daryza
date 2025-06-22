from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Producto
from authentication.models import CustomUser
from django.db.models.signals import post_save, post_delete
from gestion_almacen.models import Marca, Categoria, UnidadMedida


# @receiver(post_save, sender=Producto)
# def audit_producto_save(sender, instance, created, **kwargs):
#     # Obtener el usuario pasado a través de kwargs
#     user = kwargs.get('user', None)

#     # Si no se pasa un usuario, asignamos 'DESCONOCIDO'
#     if user is None:
#         user = 'DESCONOCIDO'
#     else:
#         user = user.username  # Asegúrate de usar el `username` si es un usuario

#     # Determinamos la acción basada en si se ha creado o actualizado el producto
#     if created:
#         accion = 'INSERTÓ'
#         descripcion = 'Creación de producto'
#     else:
#         accion = 'ACTUALIZÓ'
#         descripcion = 'Actualización de producto'

#     Auditoria.objects.create(
#         usuario_au=user,  # Aquí estamos usando el usuario o 'DESCONOCIDO'
#         tabla='Producto',
#         accion=accion,
#         registro=str(instance.id_producto),
#         nombre=instance.nombre_prod,
#         descripcion=descripcion,
#         fecha_hora=timezone.now()
#     )

# @receiver(post_delete, sender=Producto)
# def audit_producto_delete(sender, instance, **kwargs):
#     user = kwargs.get('user', 'DESCONOCIDO')  # Si no se pasa usuario, asignar 'DESCONOCIDO'

#     Auditoria.objects.create(
#         usuario_au=user,  # Aquí también usamos el usuario o 'DESCONOCIDO'
#         tabla='Producto',
#         accion='ELIMINÓ',
#         registro=str(instance.id_producto),
#         nombre=instance.nombre_prod,
#         descripcion='Eliminación de producto',
#         fecha_hora=timezone.now()
#     )
    

# @receiver(post_save, sender=Marca)
# def registrar_auditoria_marca(sender, instance, created, **kwargs):
#     # Obtener el usuario desde kwargs o usar "DESCONOCIDO" si no está disponible
#     usuario = kwargs.get('user', None)
#     if not usuario:
#         usuario = "DESCONOCIDO"

#     # Crear auditoría para la creación o actualización de la marca
#     if created:
#         descripcion = "Se ha creado una marca"
#         accion = "Crear"
#     else:
#         descripcion = "Se ha actualizado una marca"
#         accion = "Actualizar"

#     # Crear el registro en la tabla Auditoria
#     Auditoria.objects.create(
#         usuario_au=usuario.username if usuario != "DESCONOCIDO" else "DESCONOCIDO",
#         tabla="Marca",
#         accion=accion,
#         registro=str(instance.id_marca),
#         nombre=instance.nombre_marca,
#         descripcion=descripcion,
#         fecha_hora=timezone.now()
#     )

# # Signal para eliminación (pre_delete)
# @receiver(pre_delete, sender=Marca)
# def registrar_auditoria_eliminar_marca(sender, instance, **kwargs):
#     usuario = kwargs.get('user', None)
#     if not usuario:
#         usuario = "DESCONOCIDO"
    
#     # Crear auditoría para eliminación de la marca
#     Auditoria.objects.create(
#         usuario_au=usuario.username if usuario != "DESCONOCIDO" else "DESCONOCIDO",
#         tabla="Marca",
#         accion="Eliminar",
#         registro=str(instance.id_marca),
#         nombre=instance.nombre_marca,
#         descripcion="Se ha eliminado una marca",
#         fecha_hora=timezone.now()
#     )



# # Signal para UnidadMedida
# @receiver(post_save, sender=UnidadMedida)
# def registrar_auditoria_unidad_medida(sender, instance, created, **kwargs):
#     usuario = kwargs.get('user', None)
#     if usuario:
#         if created:
#             # Crear auditoría para creación
#             Auditoria.objects.create(
#                 usuario_au=usuario.username,
#                 tabla="UnidadMedida",
#                 accion="Crear",
#                 registro=str(instance.id_unidadMedida),
#                 nombre=instance.nombre_unidad,
#                 descripcion="Se ha creado una unidad de medida",
#                 fecha_hora=timezone.now()
#             )
#         else:
#             # Crear auditoría para actualización
#             Auditoria.objects.create(
#                 usuario_au=usuario.username,
#                 tabla="UnidadMedida",
#                 accion="Actualizar",
#                 registro=str(instance.id_unidadMedida),
#                 nombre=instance.nombre_unidad,
#                 descripcion="Se ha actualizado una unidad de medida",
#                 fecha_hora=timezone.now()
#             )

# # Signal para eliminación (pre_delete)
# @receiver(pre_delete, sender=UnidadMedida)
# def registrar_auditoria_eliminar_unidad_medida(sender, instance, **kwargs):
#     usuario = kwargs.get('user', None)
#     if usuario:
#         # Crear auditoría para eliminación
#         Auditoria.objects.create(
#             usuario_au=usuario.username,
#             tabla="UnidadMedida",
#             accion="Eliminar",
#             registro=str(instance.id_unidadMedida),
#             nombre=instance.nombre_unidad,
#             descripcion="Se ha eliminado una unidad de medida",
#             fecha_hora=timezone.now()
#         )
