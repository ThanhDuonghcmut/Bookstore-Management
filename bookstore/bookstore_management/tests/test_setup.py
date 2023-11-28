from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        self.books_viewing_url = reverse('books_viewing')
        self.books_modifying_url = reverse('books_modifying')
        
        return super().setUp()
    
    
    def tearDown(self) -> None:
        return super().tearDown()