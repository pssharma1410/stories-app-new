python api/manage.py migrate --noinput
python api/manage.py collectstatic --noinput
gunicorn api.wsgi:application --bind 0.0.0.0:8000 --workers 4