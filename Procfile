release: cd bookstore
release: python manage.py migrate
web: gunicorn bookstore.wsgi --log-files=-