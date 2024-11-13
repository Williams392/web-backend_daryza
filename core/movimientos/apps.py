from django.apps import AppConfig

class GestionMovimientosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movimientos'

    def ready(self):
        import movimientos.signals  # Asegúrate de importar tu archivo de signals
