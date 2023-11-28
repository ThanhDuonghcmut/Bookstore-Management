from .models import Book
from rest_framework import serializers
from cloudinary import uploader
from django.conf import settings

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publish_date', 'ISBN', 'price', 'image_url']
        

class BookSerializersImage(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publish_date', 'ISBN', 'price', 'image']
        
    def create(self, validated_data):
        result = uploader.upload(validated_data['image'], folder=settings.CLOUDINARY_FOLDER)
        book_item = Book.objects.create(
            title = validated_data['title'],
            author = validated_data['author'],
            publish_date = validated_data['publish_date'],
            ISBN = validated_data['ISBN'],
            price = validated_data['price'],
            image_public_id = result['public_id'],
            image_url = result['url']
        )
        return book_item
    
    def update(self, instance, validated_data):
        try:
            validated_data['image']
            image_id = instance.image_public_id
            if image_id != settings.EMPTY_IMAGE_PUBLIC_ID:
                uploader.destroy(image_id)
            result = uploader.upload_image(validated_data['image'], folder=settings.CLOUDINARY_FOLDER)
            instance.image_public_id = result.public_id
            instance.image_url = result.url
            instance.save()
        except KeyError:
            pass
        return super().update(instance, validated_data)
                