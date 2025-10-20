# CEMIC Autorizaciones · DO Ready

Proyecto Django + DRF con dos frontends estáticos:
- **Panel interno** en `/static/panel/index.html`
- **Formulario QR** en `/static/qr/index.html`

## Variables de entorno (.env)
Crear un archivo `.env` (o configurar en DigitalOcean App Platform) con:
```env
DJANGO_SECRET_KEY=pon-tu-clave
DEBUG=false
ALLOWED_HOSTS=*
# DATABASE_URL debe venir de tu Postgres de DO (Connection string)
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require
# Origins confiables para CSRF (si usás dominio propio)
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://app-hash.ondigitalocean.app
```

## Desarrollo local
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Docker local
```bash
cd backend
docker build -t autorizaciones .
docker run --rm -p 8080:8080       -e DJANGO_SECRET_KEY=dev       -e DEBUG=true       autorizaciones
```

## Deploy en DigitalOcean App Platform
1. Subí este repo a GitHub.
2. En DO > App Platform > Create App > From GitHub > seleccioná `backend/` como **Directorio**.
3. **Environment**: Dockerfile (ya incluido).
4. Variables de entorno:
   - `DJANGO_SECRET_KEY` (secret)
   - `DEBUG=false`
   - `DATABASE_URL` (desde tu cluster de Postgres DO)
   - `CSRF_TRUSTED_ORIGINS=https://<tu-app>.ondigitalocean.app`
5. Deploy. El contenedor ejecuta migraciones y `collectstatic` automáticamente desde `entrypoint.sh`.

## Endpoints
- GET/POST `/v1/patients/`
- PATCH/GET `/v1/patients/<id>/`
- POST `/v1/attachments/` (multipart)

## Login admin
- `/admin/`
- Cambiar contraseña: `/accounts/password_change/` (enlace accesible desde el panel)
