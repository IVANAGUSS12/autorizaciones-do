from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("core.urls")),
    # Fronts
    path("", RedirectView.as_view(url="/static/panel/index.html", permanent=False)),
    path("static/qr/", RedirectView.as_view(url="/static/qr/index.html", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
