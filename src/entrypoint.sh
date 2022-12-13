#!/bin/bash -x

python manage.py collectstatic --noinput
python manage.py migrate --noinput || exit 1
exec "$@"