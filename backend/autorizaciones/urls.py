from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from core.views_panel import panel_index, qr_index, qr_gracias, qr_i
from core.views_media import patient_file_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("core.urls")),

    # HTML
    path("panel/", panel_index, name="panel"),
    path("qr/", qr_index, name="qr"),
    path("gracias/", qr_gracias, name="qr-gracias"),

    # JSON que usa el QR para combos (coberturas, médicos, etc.)
    path("qr/i", qr_i, name="qr-i"),

    # Compatibilidad para el panel (su JS suele llamar /patients y /attachments sin /v1/)
    path("patients", lambda r: redirect("/v1/patients/", permanent=False)),
    path("attachments", lambda r: redirect("/v1/attachments/", permanent=False)),

    # Compat: links antiguos de adjuntos en el panel: /patients/<id>/<archivo>.pdf
    path("patients/<int:patient_id>/<path:filename>", patient_file_redirect, name="patient-file"),
]
