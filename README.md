# Backend Daryza 2025

Backend de gestión empresarial desarrollado con Django REST Framework.

## 📋 Tabla de Contenidos

- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración de Base de Datos](#-configuración-de-base-de-datos)
- [API Endpoints](#-api-endpoints)
- [Comandos Útiles](#-comandos-útiles)
- [Troubleshooting](#-troubleshooting)

## 🛠️ Tecnologías

- **Framework**: Django 5.0.9 + Django REST Framework
- **Base de Datos**: SQL Server (MSSQL)
- **Documentación API**: Swagger (drf-yasg)
- **Python**: 3.10.11

## 📁 Estructura del Proyecto

```bash
WEB-BACKEND_DARYZA/
├── content/                  # Archivos multimedia y data
├── venv/                     # Entorno virtual
├── core/                     # Proyecto Django principal
│   ├── content/              # Archivos de contenido
│   ├── authentication/       # Autenticación personalizada
│   ├── core/                 # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── wsgi.py
│   ├── dashboard/            # Panel de control
│   ├── gestion_almacen/      # Gestión de inventario
│   ├── gestion_venta/        # Gestión de ventas
│   ├── movimientos/          # Movimientos de inventario
│   └── manage.py
├── .env.local                # Variables de entorno (desarrollo)
├── .env.prod                 # Variables de entorno (producción)
├── .gitignore
├── README.md
└── requirements.txt          # Dependencias Python
```

## 💻 Instalación

### Prerrequisitos

- Python 3.10.11
- SQL Server o SQL Server Express
- ODBC Driver 17 for SQL Server

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd WEB-BACKEND_DARYZA
```

### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env.local` para desarrollo:

```bash
# Base de datos
DB_ENGINE=mssql
DB_NAME=BD_DARYZA_DJANGO_V7
DB_USER=sa
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=1433

# Django
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

### 5. Configurar base de datos

Editar `core/settings.py` con tus credenciales de SQL Server:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'BD_DARYZA_DJANGO_V7',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'Trusted_Connection': 'yes',
        },
    },
}
```

### 6. Ejecutar migraciones

```bash
cd core
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 8. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

### 9. Acceder a la aplicación

- **API**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **Swagger**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## 🗄️ Configuración de Base de Datos

### Migración de datos

```bash
# Hacer backup de datos existentes
python manage.py dumpdata > backup.json

# Cargar datos en nueva base
python manage.py loaddata backup.json
```

## 🔗 API Endpoints

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/signup/` - Inscribirse
- `POST /api/auth/logout/` - Cerrar sesión
- `POST /api/auth/get-api-token/` - obtener token

### Gestión de Almacén
- `GET /api/almacen/productos/` - Listar productos
- `POST /api/almacen/productos/` - Crear producto
- `PUT /api/almacen/productos/{id}/` - Actualizar producto
- `POST /api/almacen/productos/descargar/pdf/` - Descargar pdf
- `POST /api/almacen/productos/descargar/excel/` - Descargar excel

### Gestión de Ventas
- `GET /api/comprobantes/` - Listar ventas
- `GET /api/comprobantes/<str:pk>/` - Listar ventas
- `POST /api/comprobantes/pdf/<str:pk>/` - Crear venta

### Dashboard
- `GET /api/dashboard/stats/` - Estadísticas generales

*Ver documentación completa en `/swagger/`*

## 🛠️ Comandos Útiles

### Django Commands

```bash
# Crear nueva aplicación
python manage.py startapp nombre_app

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test

# Shell interactivo
python manage.py shell
```

### Base de Datos

```bash
# Reset completo de base de datos
python manage.py flush

# Mostrar migraciones
python manage.py showmigrations

# Migración específica
python manage.py migrate app_name migration_name
```

## 🔧 Troubleshooting

### Error de conexión a SQL Server

```bash
# Verificar que SQL Server esté corriendo
# Windows: Services -> SQL Server
# Verificar puerto 1433 esté abierto
netstat -an | findstr :1433
```

### Error de permisos en archivos

```bash
# En Linux/macOS, dar permisos a la carpeta de media
sudo chown -R $USER:$USER content/
chmod -R 755 content/
```

### Error de dependencias Python

```bash
# Actualizar requirements.txt
pip freeze > requirements.txt

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### CORS Issues

Verificar que las URLs del frontend estén en `CORS_ALLOWED_ORIGINS` en settings.py:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
```

## 📝 Notas de Desarrollo

- Usar siempre el entorno virtual para desarrollo local
- Los archivos de media se guardan en `content/`
- La configuración de CORS permite conexión con Angular en puerto 4200
- El proyecto usa autenticación por token JWT

## 🚀 Deployment

### Producción

1. Crear `.env.prod` con configuración de producción
2. Configurar servidor web (Apache/Nginx)
3. Configurar SSL/TLS
4. Configurar variables de entorno de producción

```bash
# Instalar dependencias en producción
pip install -r requirements.txt --no-dev

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate
```

---

**Desarrollado por**: Tu Nombre  
**Versión**: 2025.1  
**Licencia**: MIT