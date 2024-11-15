#!/usr/bin/env bash
# exit on error
set -o errexit

python3.9 pip3 install -r requirements.txt

python3.9 manage.py collectstatic --noinput 
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
if [[ $CREATE_SUPERUSER ]];
then
  python3.9 manage.py createsuperuser --noinput --email "$DJANGO_SUPERUSER_EMAIL"
fi