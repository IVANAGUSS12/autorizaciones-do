
from django.contrib import admin
from django.urls import path, re_path
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/health/", core_views.health_check, name="health"),
    path("v1/patients/", core_views.PatientsView.as_view(), name="patients"),
    path("v1/attachments/", core_views.AttachmentsView.as_view(), name="attachments"),
    re_path(r"^v1/media-signed/(?P<key>.+)$", core_views.media_signed, name="media_signed"),
    path("panel/", core_views.panel, name="panel"),
    path("qr/", core_views.qr, name="qr"),
    path("gracias/", core_views.gracias, name="gracias"),
]
