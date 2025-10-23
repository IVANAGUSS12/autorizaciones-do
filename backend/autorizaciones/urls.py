from django.contrib import admin
from django.urls import path, include
from core.views_panel import panel_index, qr_index, qr_gracias, qr_i
from core.views_media import patient_file_redirect
from core.views_compat import patients_json, attachments_json

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("core.urls")),

    # Páginas HTML
    path("panel/", panel_index, name="panel"),
    path("qr/", qr_index, name="qr"),
    path("gracias/", qr_gracias, name="qr-gracias"),
    path("qr/gracias.html", qr_gracias, name="qr-gracias-html"),  # alias para el front

    # JSON para el QR (combos)
    path("qr/i", qr_i, name="qr-i"),

    # Compat: primero archivos viejos del panel (evita capturar /patients/ list)
    path("patients/<int:patient_id>/<path:filename>", patient_file_redirect, name="patient-file"),

    # Compat: endpoints que el panel pide sin /v1 (devolvemos JSON directo; SIN redirects)
    path("patients/", patients_json, name="patients-json"),
    path("attachments/", attachments_json, name="attachments-json"),
]
