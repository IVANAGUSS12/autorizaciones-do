import os
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, FileResponse
from django.views.decorators.http import require_GET
from django.core.files.storage import default_storage

# Opcional: firma en Spaces si hay credenciales, si no, fallback a URL del storage o archivo local
try:
    import boto3
except Exception:  # pragma: no cover
    boto3 = None

SPACES_KEY = os.getenv("SPACES_KEY")
SPACES_SECRET = os.getenv("SPACES_SECRET")
SPACES_REGION = os.getenv("SPACES_REGION", "sfo3")
SPACES_ENDPOINT = os.getenv("SPACES_ENDPOINT", "https://sfo3.digitaloceanspaces.com")
SPACES_NAME = os.getenv("SPACES_NAME")


def _presign_spaces(key: str) -> str | None:
    if not (boto3 and SPACES_NAME and SPACES_KEY and SPACES_SECRET):
        return None
    try:
        session = boto3.session.Session(
            aws_access_key_id=SPACES_KEY,
            aws_secret_access_key=SPACES_SECRET,
            region_name=SPACES_REGION,
        )
        s3 = session.client("s3", endpoint_url=SPACES_ENDPOINT)
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": SPACES_NAME, "Key": key, "ResponseContentDisposition": "inline"},
            ExpiresIn=300,
        )
    except Exception:
        return None


@require_GET
def media_signed(request, object_key: str):
    """
    Devuelve una URL firmada (Spaces) o redirige a la URL del storage.
    Si el storage es local y el archivo existe, lo sirve con FileResponse.
    """
    if not object_key:
        raise Http404("Missing key")

    # 1) Intento firmar en Spaces
    url = _presign_spaces(object_key)
    if url:
        return HttpResponseRedirect(url)

    # 2) Si el storage tiene URL pública (S3 público u otro), probamos
    try:
        storage_url = default_storage.url(object_key)
        if storage_url and storage_url.startswith(("http://", "https://")):
            return HttpResponseRedirect(storage_url)
    except Exception:
        pass

    # 3) Fallback: si existe localmente, lo servimos
    if default_storage.exists(object_key):
        f = default_storage.open(object_key, "rb")
        return FileResponse(f)

    raise Http404("Archivo no encontrado")
