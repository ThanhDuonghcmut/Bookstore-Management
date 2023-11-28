from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_viewing, name='books_viewing'),
    path('books', views.books_modifying, name='books_modifying')
]
