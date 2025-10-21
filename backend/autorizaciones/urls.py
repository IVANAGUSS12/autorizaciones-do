from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Admin de Django
    path("admin/", admin.site.urls),

    # API + vistas del core
    path("v1/", include("core.urls")),

    # Raíz -> panel
    path("", RedirectView.as_view(url="/v1/panel/", permanent=False)),
]
