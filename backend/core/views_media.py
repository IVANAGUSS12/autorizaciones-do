import os
from urllib.parse import unquote
from django.http import HttpResponseRedirect, Http404, FileResponse
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Attachment

def _bucket():
    return (
        os.getenv("SPACES_BUCKET")
        or os.getenv("SPACES_NAME")
        or os.getenv("AWS_STORAGE_BUCKET_NAME")
    )

def _endpoint():
    return os.getenv("SPACES_ENDPOINT") or os.getenv("AWS_S3_ENDPOINT_URL")

def _region():
    return os.getenv("SPACES_REGION") or os.getenv("AWS_REGION") or "us-east-1"

def _client():
    try:
        import boto3  # type: ignore
    except Exception:
        return None
    ak = os.getenv("SPACES_KEY") or os.getenv("AWS_ACCESS_KEY_ID")
    sk = os.getenv("SPACES_SECRET") or os.getenv("AWS_SECRET_ACCESS_KEY")
    ep = _endpoint()
    if not (ak and sk and ep):
        return None
    session = boto3.session.Session()
    return session.client(
        "s3",
        region_name=_region(),
        endpoint_url=ep,
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
    )

def _try_presign(client, bucket, key):
    try:
        return client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=300,
            HttpMethod="GET",
        )
    except Exception:
        return None

def media_signed_view(request, key: str):
    """
    Recibe una 'key' (p.ej. 'patients/6/archivo.pdf'), maneja espacios/acentos,
    prueba variantes con/sin 'media/' y evita bucles de redirección.
    """
    original = unquote(key)

    # Variantes comunes (con/sin 'media/' y leading slash)
    candidates = [original]
    if original.startswith("/"):
        candidates.append(original.lstrip("/"))
    if original.startswith("media/"):
        candidates.append(original[len("media/"):])
    if not original.startswith("media/"):
        candidates.append("media/" + original)

    bucket = _bucket()
    client = _client()

    # 1) Firma DO Spaces / S3 (bucket privado)
    if client and bucket:
        for k in candidates:
            url = _try_presign(client, bucket, k)
            if url:
                return HttpResponseRedirect(url)

    # 2) URL directa del storage si existe (EVITANDO /patients/... para no hacer loop)
    for k in candidates:
        try:
            url = default_storage.url(k)
            if url and not url.startswith("/patients/"):
                return HttpResponseRedirect(url)
        except Exception:
            pass

    # 3) URL directa a Spaces (bucket público): dejamos que el CDN responda 200/403/404
    ep = _endpoint()
    if ep and bucket:
        for k in candidates:
            direct = f"{ep.rstrip('/')}/{bucket}/{k.lstrip('/')}"
            return HttpResponseRedirect(direct)

    # 4) Último recurso: servir desde disco (FileSystemStorage / MEDIA_ROOT)
    for k in candidates:
        try:
            path = default_storage.path(k)
            return FileResponse(open(path, "rb"))
        except Exception:
            pass
        local = os.path.join(str(getattr(settings, "MEDIA_ROOT", "/app/media")), k)
        if os.path.exists(local):
            return FileResponse(open(local, "rb"))

    raise Http404("The requested resource was not found on this server.")

def patient_file_redirect(request, patient_id: int, filename: str):
    """
    Compat para URLs antiguas del panel:
      /patients/<id>/<filename> -> /v1/media-signed/<key>
    Matchea por basename o por sufijo de 'file.name'. Evita loops.
    """
    target = unquote(filename)

    # 1) Buscar por sufijo / basename del file.name
    try:
        atts = Attachment.objects.filter(patient_id=patient_id).order_by("-created_at")
        for att in atts:
            f = getattr(att, "file", None)
            if not f:
                continue
            base = os.path.basename(f.name)
            if base == target or f.name.endswith(target):
                return HttpResponseRedirect(f"/v1/media-signed/{f.name}")
    except Exception:
        pass

    # 2) Última chance por 'name'
    try:
        att = Attachment.objects.filter(patient_id=patient_id, name=target).order_by("-created_at").first()
        if att and getattr(att, "file", None):
            return HttpResponseRedirect(f"/v1/media-signed/{att.file.name}")
    except Exception:
        pass

    raise Http404("Attachment no encontrado para ese paciente/nombre.")
