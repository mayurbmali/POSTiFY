#!/usr/bin/env bash
# Exit on error

# Install dependencies
pip3 install -r requirements.txt

# Run Django management commands

python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

python3.9 manage.py collectstatic --noinput