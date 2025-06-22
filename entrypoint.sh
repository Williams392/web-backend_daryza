# #!/bin/bash

# echo ">> Esperando que la base de datos esté lista..."

# # Esperar si usas DB en contenedor. En tu caso parece que usas MySQL local, así que puedes omitirlo o ajustarlo.

# # Aplicar migraciones automáticamente
# echo ">> Aplicando migraciones..."
# python core/manage.py makemigrations --noinput
# python core/manage.py migrate --noinput

# # Recolectar archivos estáticos (opcional)
# # python core/manage.py collectstatic --noinput

# # Iniciar servidor
# echo ">> Iniciando servidor Django..."
# exec "$@"
