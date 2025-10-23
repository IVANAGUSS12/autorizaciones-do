import os
from urllib.parse import unquote
from django.http import HttpResponseRedirect, Http404, FileResponse
from django.core.files.storage import default_storage

def _get_bucket_name():
    return (
        os.getenv("SPACES_BUCKET")
        or os.getenv("SPACES_NAME")
        or os.getenv("AWS_STORAGE_BUCKET_NAME")
    )

def _get_endpoint():
    return os.getenv("SPACES_ENDPOINT") or os.getenv("AWS_S3_ENDPOINT_URL")

def _get_region():
    return os.getenv("SPACES_REGION") or os.getenv("AWS_REGION") or "us-east-1"

def _boto3_client_or_none():
    try:
        import boto3  # type: ignore
    except Exception:
        return None
    ak = os.getenv("SPACES_KEY") or os.getenv("AWS_ACCESS_KEY_ID")
    sk = os.getenv("SPACES_SECRET") or os.getenv("AWS_SECRET_ACCESS_KEY")
    endpoint = _get_endpoint()
    if not (ak and sk and endpoint):
        return None
    session = boto3.session.Session()
    return session.client(
        "s3",
        region_name=_get_region(),
        endpoint_url=endpoint,
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
    )

def media_signed_view(request, key: str):
    # La key llega URL-encoded desde el admin → la des-encodeamos.
    key = unquote(key)

    bucket = _get_bucket_name()
    client = _boto3_client_or_none()

    # 1) Firma presignada (Spaces/S3)
    if client and bucket:
        try:
            url = client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=300,
                HttpMethod="GET",
            )
            return HttpResponseRedirect(url)
        except Exception:
            pass

    # 2) Intento vía storage.url() (si el backend lo soporta)
    try:
        url = default_storage.url(key)
        if url:
            return HttpResponseRedirect(url)
    except Exception:
        pass

    # 3) Último recurso: abrir archivo físico (p. ej. FileSystemStorage en local)
    try:
        path = default_storage.path(key)  # sólo existe en FS local
        return FileResponse(open(path, "rb"))
    except Exception:
        raise Http404("The requested resource was not found on this server.")
