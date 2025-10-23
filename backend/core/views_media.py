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

def _region():
    return os.getenv("SPACES_REGION") or os.getenv("AWS_REGION") or "sfo3"

def _endpoint():
    # usa variable si existe, si no construye https://<region>.digitaloceanspaces.com
    ep = os.getenv("SPACES_ENDPOINT") or os.getenv("AWS_S3_ENDPOINT_URL")
    if ep:
        return ep
    return f"https://{_region()}.digitaloceanspaces.com"

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
    Firma/redirige de manera robusta a un attachment:
      - soporta claves con espacios/acentos
      - prueba variantes con/sin 'media/' y leading slash
      - evita loops a /patients/...
    """
    original = unquote(key)

    candidates = [original]
    if original.startswith("/"):
        candidates.append(original.lstrip("/"))
    if original.startswith("media/"):
        candidates.append(original[len("media/"):])
    if not original.startswith("media/"):
        candidates.append("media/" + original)

    bucket = _bucket()
    client = _client()

    # 1) Presign a Spaces (privado)
    if client and bucket:
        for k in candidates:
            url = _try_presign(client, bucket, k)
            if url:
                return HttpResponseRedirect(url)

    # 2) URL del storage (evitar /patients/... para no entrar en loop)
    for k in candidates:
        try:
            url = default_storage.url(k)
            if url and not str(url).startswith("/patients/"):
                return HttpResponseRedirect(url)
        except Exception:
            pass

    # 3) URL pública directa a Spaces (si el bucket es público)
    ep = _endpoint()
    if ep and bucket:
        for k in candidates:
            direct = f"{ep.rstrip('/')}/{bucket}/{k.lstrip('/')}"
            return HttpResponseRedirect(direct)

    # 4) Servir desde disco (FileSystemStorage / MEDIA_ROOT)
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
    Matchea por basename o por sufijo del file.name.
    """
    from urllib.parse import unquote as _unq
    import os as _os
    target = _unq(filename)

    try:
        atts = Attachment.objects.filter(patient_id=patient_id).order_by("-created_at")
        for att in atts:
            f = getattr(att, "file", None)
            if not f:
                continue
            base = _os.path.basename(f.name)
            if base == target or f.name.endswith(target):
                return HttpResponseRedirect(f"/v1/media-signed/{f.name}")
    except Exception:
        pass

    try:
        att = Attachment.objects.filter(patient_id=patient_id, name=target).order_by("-created_at").first()
        if att and getattr(att, "file", None):
            return HttpResponseRedirect(f"/v1/media-signed/{att.file.name}")
    except Exception:
        pass

    raise Http404("Attachment no encontrado para ese paciente/nombre.")

