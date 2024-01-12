#!/bin/bash
# Entry point for Docker run
set -euo pipefail
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py cicore_init
exec python -m gunicorn citadel.wsgi -b 0:$PORT -w 5
