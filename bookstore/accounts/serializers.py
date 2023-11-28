from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserRegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    confirmed_password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirmed_password']
        
    def validate(self, attrs):
        password = attrs.get('password', '')
        confirmed_password = attrs.get('confirmed_password', '')
        if password != confirmed_password:
            raise serializers.ValidationError('password do not match')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
    
class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token']
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request=request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credential, try again')
        token = user.tokens()
        
        return {
            'email': user.email,
            'name': user.name,
            'access_token': token['access'],
            'refresh_token': token['refresh']
        }
        
class LogoutSerializers(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
