
from pathlib import Path
import os
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core ---
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
        "DIRS": [BASE_DIR / "core" / "templates"],
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

# --- Database ---
def db_from_url(url: str):
    # Supports postgres://user:pass@host:port/dbname?sslmode=require
    parsed = urlparse(url)
    if parsed.scheme not in ("postgres", "postgresql"):
        raise ValueError("Unsupported DATABASE_URL scheme")
    qs = parse_qs(parsed.query or "")
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": (parsed.path or "/")[1:] or os.getenv("DB_NAME", "autorizaciones"),
        "USER": parsed.username or os.getenv("DB_USER", ""),
        "PASSWORD": parsed.password or os.getenv("DB_PASSWORD", ""),
        "HOST": parsed.hostname or os.getenv("DB_HOST", ""),
        "PORT": str(parsed.port or os.getenv("DB_PORT", "5432")),
        "OPTIONS": {
            # Honor sslmode if provided
            **({"sslmode": qs.get("sslmode", [""])[0]} if qs.get("sslmode") else {})
        },
    }

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DB_URL")
if DATABASE_URL:
    try:
        DATABASES = {"default": db_from_url(DATABASE_URL)}
    except Exception:
        # Fallback to discrete envs if parsing fails
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("DB_NAME", "autorizaciones"),
                "USER": os.getenv("DB_USER", "postgres"),
                "PASSWORD": os.getenv("DB_PASSWORD", ""),
                "HOST": os.getenv("DB_HOST", ""),
                "PORT": os.getenv("DB_PORT", "5432"),
            }
        }
else:
    # Explicit envs (DO Managed DB: set DB_HOST to the managed host, not localhost)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "autorizaciones"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", ""),  # e.g. db-postgresql-xxxx.do-user-xxxx.c.db.ondigitalocean.com
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

# --- Static / WhiteNoise ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

_core_static = BASE_DIR / "core" / "static"
STATICFILES_DIRS = [_core_static] if _core_static.exists() else []

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Files ---
DEFAULT_FILE_STORAGE = os.getenv("DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage")

# --- Misc ---
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Health path (used by DO health check)
APP_HEALTHCHECK_PATH = os.getenv("APP_HEALTHCHECK_PATH", "/v1/health/")
