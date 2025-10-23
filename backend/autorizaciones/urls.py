from django.contrib import admin
from django.urls import path, include
from core.health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    # Readiness para DO
    path("v1/health/", health_check, name="health_check"),
    # El resto de tus rutas (API v1, panel, qr, etc.) ya definidas en core/urls.py
    path("", include("core.urls")),
]
