#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-autorizaciones.settings}
export PORT=${PORT:-8080}

echo "⏳ Esperando DB..."
sleep 2

echo "⚙️ Migraciones"
python -m django makemigrations --noinput || true
python -m django migrate --noinput

echo "📦 collectstatic"
python -m django collectstatic --noinput || true

echo "🚀 Gunicorn"
exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:${PORT} --workers ${GUNICORN_WORKERS:-3} --timeout 120
