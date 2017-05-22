#!/bin/bash
# Entry point for Docker run
set -euo pipefail
python manage.py migrate
python manage.py collectstatic --noinput
exec $HOME/.local/bin/gunicorn citadel.wsgi -b 0:$PORT -w 5
