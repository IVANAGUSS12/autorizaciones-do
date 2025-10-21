from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin normal
    path("admin/", admin.site.urls),

    # API
    path("v1/", include("core.urls")),
]

# NO redirigimos "/" a ningún lado: /static/... lo sirve WhiteNoise directo.
