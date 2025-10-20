# backend/autorizaciones/settings.py
from pathlib import Path
import os
from decouple import config
import dj_database_url

# -------------------------
# Paths / Base
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# Seguridad / Debug
# -------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="change-me")
DEBUG = config("DEBUG", default=False, cast=bool)

# Podés dejarlo así o tomarlo de env con una coma separada
ALLOWED_HOSTS = (
    config("ALLOWED_HOSTS", default="starfish-app-putz9.ondigitalocean.app")
    .split(",")
)

CSRF_TRUSTED_ORIGINS = [
    "https://starfish-app-putz9.ondigitalocean.app",
]

# Si usás proxy/https atrás de DO
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Permitir iframes (para previsualizar adjuntos en el panel)
X_FRAME_OPTIONS = "SAMEORIGIN"

# -------------------------
# Apps
# -------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "storages",            # para DigitalOcean Spaces

    # Apps del proyecto
    "core",
]

# -------------------------
# Middleware
# -------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "autorizaciones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "autorizaciones.wsgi.application"

# -------------------------
# Base de Datos (DATABASE_URL)
# -------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# -------------------------
# Passwords
# -------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------
# I18N
# -------------------------
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# -------------------------
# Static & Media
#  - STATIC: locales (collectstatic en DO)
#  - MEDIA : DigitalOcean Spaces
# -------------------------

# STATIC locales (App Platform sirve /app/staticfiles)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Si tenés assets en /static dentro de apps, no hace falta STATICFILES_DIRS

# MEDIA en Spaces (solo MEDIA, NO los static)
AWS_ACCESS_KEY_ID = config("SPACES_KEY", default="")
AWS_SECRET_ACCESS_KEY = config("SPACES_SECRET", default="")
AWS_STORAGE_BUCKET_NAME = config("SPACES_NAME", default="autorizaciones-media")
AWS_S3_REGION_NAME = config("SPACES_REGION", default="sfo3")

# Endpoint S3 de DO (sin el bucket)
AWS_S3_ENDPOINT_URL = "https://sfo3.digitaloceanspaces.com"

# Dominio público del bucket (virtual hosted–style)
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.sfo3.digitaloceanspaces.com"
AWS_S3_ADDRESSING_STYLE = "virtual"       # bucket.sfo3.digitaloceanspaces.com
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True               # URLs firmadas (bucket privado)

# Storage por defecto SOLO para MEDIA
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# URL pública de media
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
# No se usa en producción con Spaces, pero no estorba:
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------
# DRF
# -------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------
# Otros
# -------------------------
APPEND_SLASH = True
