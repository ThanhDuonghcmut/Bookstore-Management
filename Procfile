release: python bookstore/manage.py migrate
web: cd bookstore && gunicorn bookstore.wsgi:application --log-file=-