#!/bin/sh
set -e
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-autorizaciones.settings}
mkdir -p /workspace /workspace/staticfiles /workspace/data/media
python -m django migrate --noinput
python -m django collectstatic --noinput || true
exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers ${GUNICORN_WORKERS:-3} --timeout 120
