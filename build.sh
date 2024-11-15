#!/usr/bin/env bash
# Exit on error
set -o errexit

# Activate the virtual environment
source C:/Users/Mayur Mali/djangoEnv/Scripts/activate

# Install dependencies
pip3 install -r requirements.txt

# Run Django management commands
python3.9 manage.py collectstatic --noinput
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

# Create superuser if required
if [[ $CREATE_SUPERUSER ]]; then
  python3.9 manage.py createsuperuser --noinput --email "$DJANGO_SUPERUSER_EMAIL"
fi
