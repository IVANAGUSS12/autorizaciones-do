import os
import boto3
from django.http import HttpResponseRedirect, HttpResponseBadRequest

SPACES_KEY = os.getenv("SPACES_KEY")
SPACES_SECRET = os.getenv("SPACES_SECRET")
SPACES_REGION = os.getenv("SPACES_REGION", "sfo3")
SPACES_NAME = os.getenv("SPACES_NAME")

session = boto3.session.Session()
s3 = session.client(
    "s3",
    region_name=SPACES_REGION,
    endpoint_url=f"https://{SPACES_REGION}.digitaloceanspaces.com",
    aws_access_key_id=SPACES_KEY,
    aws_secret_access_key=SPACES_SECRET,
)

def media_signed_redirect(request, path):
    """
    Redirige a una URL firmada de Spaces para el objeto 'path'.
    path es el key que guardás en tu modelo (ej: patients/2/archivo.pdf)
    """
    if not path:
        return HttpResponseBadRequest("missing path")

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": SPACES_NAME, "Key": path},
        ExpiresIn=300,  # 5 minutos
    )
    return HttpResponseRedirect(url)
