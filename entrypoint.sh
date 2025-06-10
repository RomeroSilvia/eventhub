#!/bin/sh


echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate
python manage.py migrate cities_light
python manage.py loaddata fixtures/*.json

echo "Iniciando servidor Gunicorn..."
exec "$@"