from accounts.models import User
from django.urls import reverse
from .test_setup import TestSetUp

class TestModel(TestSetUp):
    def setUp(self):
        self.user = User.objects.create(
            email = 'test@gmail.com',
            name = 'test'
        )
        self.user.set_password('12345678')
        return super().setUp()
    
    def test_wrong_user_access_token_with_logout(self):
        token = self.user.tokens()
        
        logout_data = {'refresh_token': token['refresh']}
        access_token = 'Bearer  ' + 'wrong_token'
        
        res = self.client.post(self.logout_url, logout_data, headers={'authorization': access_token})
        
        self.assertEqual(res.status_code, 401)
        
    def test_wrong_user_refresh_token_with_logout(self):
        token = self.user.tokens()
        
        logout_data = {'refresh_token': 'wrong_token'}
        access_token = 'Bearer  ' + token['access']
        
        res = self.client.post(self.logout_url, logout_data, headers={'authorization': access_token})
        
        self.assertEqual(res.status_code, 400)
        
    def test_true_user_token_with_logout(self):
        token = self.user.tokens()
        
        logout_data = {'refresh_token': token['refresh']}
        access_token = 'Bearer  ' + token['access']
        
        res = self.client.post(self.logout_url, logout_data, headers={'authorization': access_token})
        
        self.assertEqual(res.status_code, 204)
        