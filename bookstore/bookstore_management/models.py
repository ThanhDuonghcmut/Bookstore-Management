from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    publish_date = models.DateField()
    ISBN = models.CharField(max_length=20)
    price = models.FloatField()
    
    