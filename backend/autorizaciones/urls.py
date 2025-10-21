from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("v1/", include("core.urls")),
    # Redirección de la raíz al panel estático
    path("", RedirectView.as_view(url="/static/panel/index.html", permanent=False)),
]
