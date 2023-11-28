from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializers, BookSerializersImage
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
def books_viewing(request):
    id = request.query_params.get('id')
    if id:
        book_items = BookSerializers([get_object_or_404(Book, id=id)], many=True).data
        num_items = 1
        num_pages = 1
    else:
        perpage = request.query_params.get('limit')
        page = request.query_params.get('page')
        if not perpage:
            perpage = 5
        if not page:
            page = 1
        search_key = request.query_params.get('key')
        items = Book.objects.all()
        if search_key:
            items = items.filter(author__icontains=search_key) | items.filter(title__icontains=search_key)
        paginator = Paginator(items.order_by('id'), per_page=perpage)
        num_items = len(items)
        num_pages = paginator.num_pages
        try:
            book_items = BookSerializers(paginator.page(number=page), many=True).data
        except EmptyPage:
            book_items = []
    return Response({'data': book_items, 'total_items': num_items, 'total_pages': num_pages, 'message': 'GET books successfully'}, status=status.HTTP_200_OK)
        
        
@api_view(['POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def books_modifying(request):
    if request.method == 'POST':
        data = request.data
        try:
            data['image']
            book_serializer = BookSerializersImage(data=data)
        except KeyError:
            book_serializer = BookSerializers(data=data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response({'message': 'ADD new book successfully'}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'PATCH':
        id = request.query_params.get('id')
        if not id:
            return Response({'message': 'CANNOT get ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=id)
            book_serializer = BookSerializersImage(book, data=request.data, partial=True)
            book_serializer.is_valid(raise_exception=True)
            book_serializer.save()
            return Response({'message': f'UPDATE book ID {id} successfully'}, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'message': f'Book with ID {id} DOESN\'T exist'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        id = request.query_params.get('id')
        if not id:
            return Response({'message': 'CANNOT get ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book_item = Book.objects.get(id=id)
            book_item.delete()
            return Response({'message': f'DELETE book ID {id} successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({'message': f'Book with ID {id} DOESN\'T exist'}, status=status.HTTP_404_NOT_FOUND)
    