from django.contrib import admin
from django.urls import path, include
from core.views_panel import panel_index, qr_index, qr_gracias, qr_i
from core.views_media import patient_file_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("core.urls")),

    # HTML
    path("panel/", panel_index, name="panel"),
    path("qr/", qr_index, name="qr"),
    path("gracias/", qr_gracias, name="qr-gracias"),
    path("qr/gracias.html", qr_gracias, name="qr-gracias-html"),  # alias para el front

    # JSON que usa el QR (combos)
    path("qr/i", qr_i, name="qr-i"),

    # Compat para links viejos del panel:
    # /patients/<id>/<archivo>.pdf -> redirige a /v1/media-signed/<key>
    path("patients/<int:patient_id>/<path:filename>", patient_file_redirect, name="patient-file"),
]
