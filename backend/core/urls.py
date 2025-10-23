from django.urls import path
from .views import health_check

# OJO: mantené aquí todas tus rutas actuales (patients, attachments, media-signed, etc.)
# Debajo agregamos health/ para que /v1/health/ exista también desde core si lo preferís así.

urlpatterns = [
    path("health/", health_check, name="health_check_core"),
    # ... (tus rutas existentes) ...
]
