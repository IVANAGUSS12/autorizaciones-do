#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-autorizaciones.settings}"
export PORT="${PORT:-8080}"

echo "🚀 Esperando la base de datos..."
sleep 3

echo "⚙️ Aplicando migraciones..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || true

echo "✅ Iniciando servidor..."
exec gunicorn autorizaciones.wsgi:application --bind 0.0.0.0:$PORT --timeout 90
