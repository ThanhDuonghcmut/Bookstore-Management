from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        
        self.full_user_register = {
            'email': 'test@gmail.com',
            'name': 'test',
            'password': '12345678',
            'confirmed_password': '12345678'
        }
        
        self.true_user_login = {
            'email': 'test@gmail.com',
            'password': '12345678'
        }
        
        return super().setUp()
    
    
    def tearDown(self) -> None:
        return super().tearDown()