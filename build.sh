#!/usr/bin/env bash
# exit on error
set -o errexit

python pip3 install -r requirements.txt

python manage.py collectstatic --noinput 
python manage.py makemigrations --noinput
python manage.py migrate --noinput
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --noinput --email "$DJANGO_SUPERUSER_EMAIL"
fi