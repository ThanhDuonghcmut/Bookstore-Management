from django.db import models
from django.conf import settings

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    publish_date = models.DateField()
    ISBN = models.CharField(max_length=20)
    price = models.FloatField()
    image_public_id = models.CharField(max_length=100, default=settings.EMPTY_IMAGE_PUBLIC_ID)
    image_url = models.CharField(max_length=512, default=settings.EMPTY_IMAGE_URL)
 