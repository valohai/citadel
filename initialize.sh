#!/bin/bash
# First-run tasks to be done within Docker container
set -xeuo pipefail
python manage.py migrate
python manage.py createsuperuser
