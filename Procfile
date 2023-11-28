release: python bookstore/manage.py migrate
web: gunicorn bookstore.wsgi:application --log-file=-