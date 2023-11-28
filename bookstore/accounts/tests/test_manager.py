from accounts.manager import UserManager
from django.urls import reverse
from .test_setup import TestSetUp

class TestManager(TestSetUp):
    def setUp(self):
        self.manager = UserManager()
        return super().setUp()
    
    def test_email_validator(self):      
        email = 'test'
        args = [email]
        self.assertRaises(ValueError, self.manager.email_validator, *args)
        
        email = 'test@a.b'
        args = [email]
        self.assertRaises(ValueError, self.manager.email_validator, *args)
        
        email = 'test@gmail.com'
        self.assertEqual(self.manager.email_validator(email), None)
        
    def test_create_user_missing_parameters(self):
        missing_email_args = [None, 'test', '12345678']
        self.assertRaises(ValueError, self.manager.create_user, *missing_email_args)
        
        missing_name_args = ['test@gmail.com', None, '12345678']
        self.assertRaises(ValueError, self.manager.create_user, *missing_name_args)