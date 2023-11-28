from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserRegisterSerializers, LoginSerializers, LogoutSerializers
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['POST'])
def registration(request):
    user_data = request.data
    serializers = UserRegisterSerializers(data=user_data)
    
    if serializers.is_valid(raise_exception=True):
        serializers.save()
        user = serializers.data
        return Response({'message': 'Register new user successfully', 'data': user}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Data is invalid'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    data = request.data
    serializers = LoginSerializers(data=data, context={'request': request})
    serializers.is_valid(raise_exception=True)
    return Response({'message': 'LOGIN successfully', 'data': serializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    data = request.data
    serializers = LogoutSerializers(data=data)
    serializers.is_valid(raise_exception=True)
    serializers.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response(data='OK')