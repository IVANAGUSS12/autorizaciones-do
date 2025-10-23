
from django.contrib import admin
from django.urls import path, include
from core.views_panel import panel_index, qr_index, qr_gracias

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("core.urls")),
    path("panel/", panel_index, name="panel"),
    path("qr/", qr_index, name="qr"),
    path("gracias/", qr_gracias, name="qr-gracias"),
]
