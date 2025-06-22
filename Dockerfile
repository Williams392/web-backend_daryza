# Dockerfile
FROM python:3.10.11 AS backend

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Copiar requirements y instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . /app/

# Crear directorio para archivos estáticos y media
RUN mkdir -p /app/staticfiles /app/content

# Exponer puerto
EXPOSE 8000

# Comando por defecto
#RUN chmod +x /app/entrypoint.sh
CMD ["python", "core/manage.py", "runserver", "0.0.0.0:8000"]