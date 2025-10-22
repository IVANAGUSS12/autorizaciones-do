from django.contrib import admin
from django.urls import path, include
# (opcional) si querés servir /panel/ y /qr/:
# from core.views_panel import panel_index, qr_index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("core.urls")),
    # Opcional:
    # path("panel/", panel_index, name="panel"),
    # path("qr/", qr_index, name="qr"),
]
