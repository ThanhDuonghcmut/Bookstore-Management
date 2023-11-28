from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Please enter a valid email address')
        
        
    def create_user(self, email, name, password, **extras_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError('please enter an email address')
        
        if not name:
            raise ValueError('please enter your name')
        
        user = self.model(email=email, name=name, **extras_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, name, password, **extras_fields):
        extras_fields.setdefault('is_staff', True)
        extras_fields.setdefault('is_superuser', True)
        
        if extras_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True for admin user')
        
        if extras_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True for admin user')
        
        user = self.create_user(email, name, password, **extras_fields)
        user.save()
        return user