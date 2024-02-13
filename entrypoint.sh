#!/bin/sh

cd app

echo "----- Collect static files ------ " 
python manage.py collectstatic --no-input

echo "-----------Apply migration--------- "
python manage.py makemigrations && python manage.py migrate --no-input

echo "-----------Run --------- "
gunicorn app.wsgi:application --bind 0.0.0.0:8000