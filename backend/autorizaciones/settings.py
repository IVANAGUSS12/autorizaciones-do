import os
from pathlib import Path
from datetime import timedelta

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Core ===
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PROD")
DEBUG = os.getenv("DEBUG", "0") == "1"

# ALLOWED_HOSTS: coma-separado → "app1.com,app2.com"
ALLOWED_HOSTS = [h for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h] or ["*"]

# === Apps ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party
    "rest_framework",
    "storages",        # django-storages para DigitalOcean Spaces

    # apps propias
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise para servir estáticos en DO
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

# === Database ===
# Usa DATABASE_URL (Postgres en DO) o SQLite en dev.
# Ejemplo DATABASE_URL:
# postgres://USER:PASSWORD@HOST:PORT/DB_NAME
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=os.getenv("DB_SSL_REQUIRE", "1") == "1",
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# === Passwords / Auth ===
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# === Internacionalización ===
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# === Static / Media ===
# WhiteNoise (admin y assets del front)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media en DigitalOcean Spaces (django-storages + boto3)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Variables de Spaces desde ENV (DEBES CARGARLAS EN DO)
AWS_S3_REGION_NAME = os.getenv("SPACES_REGION", "sfo3")
AWS_S3_ENDPOINT_URL = os.getenv("SPACES_ENDPOINT", "https://sfo3.digitaloceanspaces.com")
AWS_STORAGE_BUCKET_NAME = os.getenv("SPACES_NAME")  # nombre exacto del bucket

# Estilo y firma
AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_S3_SIGNATURE_VERSION = "s3v4"

# Recomendado con media firmada y bucket privado:
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True

# Si prefirieras objetos públicos (no recomendado):
# AWS_DEFAULT_ACL = "public-read"
# AWS_QUERYSTRING_AUTH = False

# === Seguridad básica (prod) ===
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "1") == "1"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "1") == "1"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))  # p.ej. 31536000 en prod
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "0") == "1"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "0") == "1"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "1") == "1"

# CSRF / CORS (para panel/QR en DO App)
# Agregamos dominios típicos de DO App Platform
CSRF_TRUSTED_ORIGINS = [
    "https://*.ondigitalocean.app",
    "https://*.digitaloceanspaces.com",
    # Agregá tu URL pública si querés ser explícito:
    # "https://starfish-app-putz9.ondigitalocean.app",
]
# Si usás django-cors-headers, podés sumar:
# CORS_ALLOWED_ORIGINS = [
#     "https://starfish-app-putz9.ondigitalocean.app",
# ]

# === DRF básico ===
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Nota: para los endpoints públicos (QR) ya sacamos auth en las viewsets
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# === Logging (útil en DO) ===
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO")},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
