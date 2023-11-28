release: python bookstore/manage.py migrate
web: gunicorn bookstore/bookstore.wsgi:application --log-file=-