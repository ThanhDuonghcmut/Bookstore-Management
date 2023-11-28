from .test_setup import TestSetUp
from rest_framework.serializers import ValidationError

# Create your tests here.
class TestViews(TestSetUp):
    def test_user_cannot_register_with_missing_information(self):
        missing_name_register = {
            'email': 'test1@gmail.com',
            'password': '12345678',
            'confirmed_password': '12345678'
        }
        
        missing_email_register = {
            'name': 'test',
            'password': '12345678',
            'confirmed_password': '12345678'
        }
        
        missing_confirmed_password_register = {
            'email': 'test@gmail.com',
            'name': 'test',
            'password': '12345678'
        }
        
        wrong_email_format_register = {
            'email': 'test1@a.b',
            'name': 'test',
            'password': '12345678',
            'confirmed_password': '12345678'
        }
        
        res1 = self.client.post(self.register_url)
        res2 = self.client.post(self.register_url, missing_name_register)
        res3 = self.client.post(self.register_url, missing_email_register)
        res4 = self.client.post(self.register_url, missing_confirmed_password_register)
        res5 = self.client.post(self.register_url, wrong_email_format_register)
        
        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res3.status_code, 400)
        self.assertEqual(res4.status_code, 400)
        self.assertEqual(res5.status_code, 400)
        
    def test_user_register_with_wrong_confirmed_password(self):
        wrong_confirmed_password_register = {
            'email': 'test1@gmail.com',
            'name': 'test',
            'password': '12345678',
            'confirmed_password': '12345679'
        }
        res = self.client.post(self.register_url, wrong_confirmed_password_register)
        
        self.assertEqual(res.status_code, 400)
        
    def test_user_can_register(self):
        res = self.client.post(self.register_url, self.full_user_register)
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['data']['email'], self.full_user_register['email'])
        self.assertEqual(res.data['data']['name'], self.full_user_register['name'])
        
    
    def test_user_login_without_registration(self):
        res = self.client.post(self.login_url, self.true_user_login)
        
        self.assertEqual(res.status_code, 401)
        
    def test_user_can_login(self):
        self.client.post(self.register_url, self.full_user_register)
        res = self.client.post(self.login_url, self.true_user_login)
        
        self.assertEqual(res.status_code, 200)
        
    def test_user_cannot_login_with_wrong_information(self):
        wrong_email_login = {
            'email': 'test1@gmail.com',
            'password': '12345678'
        }
        
        wrong_password_login = {
            'email': 'test@gmail.com',
            'password': '12345679'
        }
        
        self.client.post(self.register_url, self.full_user_register)
        res1 = self.client.post(wrong_email_login)
        res2 = self.client.post(wrong_password_login)
        
        self.assertEqual(res1.status_code, 404)
        self.assertEqual(res2.status_code, 404)
        
    
    def test_user_cannot_logout_without_login(self):
        self.client.post(self.register_url, self.full_user_register)
        res = self.client.post(self.logout_url)
        
        self.assertEqual(res.status_code, 401)
        
    def test_user_cannot_logout_without_true_access_token(self):
        self.client.post(self.register_url, self.full_user_register)
        login_res = self.client.post(self.login_url, self.true_user_login)
        
        logout_data = {'refresh_token': login_res.data['data']['refresh_token']}
        access_token = 'Bearer  ' + 'wrong_token' 
        
        res = self.client.post(self.logout_url, logout_data, headers={'authorization': access_token})
        
        self.assertEqual(res.status_code, 401)
        
    def test_user_logout_with_wrong_refresh_token(self):
        self.client.post(self.register_url, self.full_user_register)
        login_res = self.client.post(self.login_url, self.true_user_login)
        
        logout_data = {'refresh_token': 'wrong_token'}
        access_token = 'Bearer  ' + login_res.data['data']['access_token'] 
        
        res = self.client.post(self.logout_url, logout_data, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 400)
        
    def test_user_can_logout(self):
        self.client.post(self.register_url, self.full_user_register)
        login_res = self.client.post(self.login_url, self.true_user_login)
        
        logout_data = {'refresh_token': login_res.data['data']['refresh_token']}
        access_token = 'Bearer  ' + login_res.data['data']['access_token'] 
        
        res = self.client.post(self.logout_url, logout_data, headers={'authorization': access_token})
        
        self.assertEqual(res.status_code, 204)
    
        