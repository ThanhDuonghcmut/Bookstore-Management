from .test_setup import TestSetUp
from bookstore_management.models import Book
from accounts.models import User
import datetime
from datetime import datetime as dt

# Create your tests here.
class TestBookView(TestSetUp):
    def setUp(self):
        Book.objects.create(
            title = 'Little Red Riding Hood',
            author = 'Grimme',
            publish_date = datetime.date(2023, 12, 24),
            ISBN = '123-45-678',
            price = 12.5
        )
        
        Book.objects.create(
            title = 'Snow White and 7 Dwarfs',
            author = 'Grimme',
            publish_date = datetime.date(1999, 1, 15),
            ISBN = '123-45-123',
            price = 20.0
        )
        
        Book.objects.create(
            title = 'Naruto Dattebayo',
            author = 'Kishimoto Masashi',
            publish_date = datetime.date(2010, 2, 20),
            ISBN = '123-89-123',
            price = 15.0
        )
        
        return super().setUp()
    
    def test_book_viewing(self):
        res = self.client.get(self.books_viewing_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['data']), 3)
        self.assertEqual(res.data['total_items'], 3)
        self.assertEqual(res.data['total_pages'], 1)
        
    def test_book_viewing_with_ID(self):
        res = self.client.get(self.books_viewing_url, {'id': 1})
        data_test = {
            'id': 1,
            'title': 'Little Red Riding Hood',
            'author': 'Grimme',
            'publish_date': '2023-12-24',
            'ISBN': '123-45-678',
            'price': 12.5
        }
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data['data'][0], data_test)
        self.assertEqual(res.data['total_items'], 1)
        self.assertEqual(res.data['total_pages'], 1)
        
    def test_book_viewing_with_paginator(self):
        res = self.client.get(self.books_viewing_url, {'limit': 2, 'page': 1})
        data_test = {
            'id': 1,
            'title': 'Little Red Riding Hood',
            'author': 'Grimme',
            'publish_date': '2023-12-24',
            'ISBN': '123-45-678',
            'price': 12.5
        }
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data['data'][0], data_test)
        self.assertEqual(len(res.data['data']), 2)
        self.assertEqual(res.data['total_items'], 3)
        self.assertEqual(res.data['total_pages'], 2)
        
    def test_book_viewing_with_key_search(self):
        res = self.client.get(self.books_viewing_url, {'key': 'Grimme'})
        data_test = [
        {
            'id': 1,
            'title': 'Little Red Riding Hood',
            'author': 'Grimme',
            'publish_date': '2023-12-24',
            'ISBN': '123-45-678',
            'price': 12.5
        },
        {
            'id': 2,
            'title': 'Snow White and 7 Dwarfs',
            'author': 'Grimme',
            'publish_date': '1999-01-15',
            'ISBN': '123-45-123',
            'price': 20.0            
        }
        ]

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.data['data'][0], data_test[0])
        self.assertDictEqual(res.data['data'][1], data_test[1])
        self.assertEqual(len(res.data['data']), 2)
        self.assertEqual(res.data['total_items'], 2)
        
    def test_book_viewing_with_ID_out_of_range(self):
        res = self.client.get(self.books_viewing_url, {'id': 4})
        self.assertEqual(res.status_code, 404)
        
    def test_book_viewing_page_out_of_range(self):
        res = self.client.get(self.books_viewing_url, {'limit': 2, 'page': 3})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['data'], [])
        self.assertEqual(res.data['total_items'], 3)
        self.assertEqual(res.data['total_pages'], 2)
        

class TestBookModifying(TestSetUp):
    def setUp(self):
        self.true_user_login = {
            'email': 'test@gmail.com',
            'password': '12345678'
        }
        
        self.full_user_register = {
            'email': 'test@gmail.com',
            'name': 'test',
            'password': '12345678',
            'confirmed_password': '12345678'
        }
        
        Book.objects.create(
            title = 'Little Red Riding Hood',
            author = 'Grimme',
            publish_date = datetime.date(2023, 12, 24),
            ISBN = '123-45-678',
            price = 12.5
        )
        
        Book.objects.create(
            title = 'Snow White and 7 Dwarfs',
            author = 'Grimme',
            publish_date = datetime.date(1999, 1, 15),
            ISBN = '123-45-123',
            price = 20.0
        )
        
        return super().setUp()
    
    def test_books_modifying_without_login_POST_PUT_DELETE(self):
        new_book_data = {
            'title': 'Naruto Dattebayo',
            'author': 'Kishimoto Masashi',
            'publish_date': '2010-02-20',
            'ISBN': '123-89-123',
            'price': 15.0
        }
        
        res = self.client.post(self.books_modifying_url, new_book_data)
        self.assertEqual(res.status_code, 401)
        
        update_data = {
            'title': 'Little Red Riding Hood',
            'author': 'Grimme',
            'publish_date': '2023-12-24',
            'ISBN': '123-45-765',
            'price': 30.5
        }
        
        res = self.client.put(self.books_modifying_url, update_data, **{'id': 1})
        self.assertEqual(res.status_code, 401)
        
        res = self.client.delete(self.books_modifying_url, {'id': 1})
        self.assertEqual(res.status_code, 401)
        
    
    def test_books_modifying_add_new_book_successfully(self):
        self.client.post(self.register_url, self.full_user_register)
        res_login = self.client.post(self.login_url, self.true_user_login)
        access_token = 'Bearer  ' + res_login.data['data']['access_token'] 
        
        new_book_data = {
            'title': 'Naruto Dattebayo',
            'author': 'Kishimoto Masashi',
            'publish_date': '2010-02-20',
            'ISBN': '123-89-123',
            'price': 15.0
        }
        
        res = self.client.post(self.books_modifying_url, new_book_data, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 201)
        
        book = Book.objects.filter(title=new_book_data['title']).first()
        self.assertEqual(book.title, new_book_data['title'])
        self.assertEqual(book.author, new_book_data['author'])
        self.assertEqual(book.ISBN, new_book_data['ISBN'])
        self.assertEqual(book.price, new_book_data['price'])
        publish_date = dt.strptime(new_book_data['publish_date'], '%Y-%m-%d').date()
        self.assertEqual(book.publish_date, publish_date)
        
    def test_books_modifying_update_without_ID(self):
        self.client.post(self.register_url, self.full_user_register)
        res_login = self.client.post(self.login_url, self.true_user_login)
        access_token = 'Bearer  ' + res_login.data['data']['access_token']
        
        update_data = {
            'title': 'Alice in Wonderland',
            'publish_date': '1993-12-24',
            'ISBN': '123-45-765',
            'price': 30.5
        }
        
        res = self.client.patch(self.books_modifying_url, update_data, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 400)
        
    def test_books_modifying_update_with_ID_not_exist(self):
        self.client.post(self.register_url, self.full_user_register)
        res_login = self.client.post(self.login_url, self.true_user_login)
        access_token = 'Bearer  ' + res_login.data['data']['access_token']
        
        update_data = {
            'title': 'Alice in Wonderland',
            'publish_date': '1993-12-24',
            'ISBN': '123-45-765',
            'price': 30.5
        }
        
        url = self.books_modifying_url + '?id=3'
        
        res = self.client.patch(url, update_data, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 404)
        
    def test_books_modifying_update_book_successfully(self):
        self.client.post(self.register_url, self.full_user_register)
        res_login = self.client.post(self.login_url, self.true_user_login)
        access_token = 'Bearer  ' + res_login.data['data']['access_token']
        
        update_data = {
            'author': 'Grimme',
            'title': 'Alice in Wonderland',
            'publish_date': '1993-12-24',
            'ISBN': '123-45-765',
            'price': 30.5
        }
        
        id = 1
        url = self.books_modifying_url + '?id=' + str(id)
        res = self.client.patch(url, update_data, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 201)
        
        book = Book.objects.get(id=id)
        self.assertEqual(book.title, update_data['title'])
        self.assertEqual(book.author, 'Grimme')
        self.assertEqual(book.ISBN, update_data['ISBN'])
        self.assertEqual(book.price, update_data['price'])
        publish_date = dt.strptime(update_data['publish_date'], '%Y-%m-%d').date()
        self.assertEqual(book.publish_date, publish_date)
        
        
    def test_book_modifying_delete_book_with_ID_not_exist(self):
        self.client.post(self.register_url, self.full_user_register)
        res_login = self.client.post(self.login_url, self.true_user_login)
        access_token = 'Bearer  ' + res_login.data['data']['access_token']
        
        id = 3
        url = self.books_modifying_url + '?id=' + str(id)
        res = self.client.delete(url, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 404)
        
    def test_book_modifying_delete_book_successfully(self):
        self.client.post(self.register_url, self.full_user_register)
        res_login = self.client.post(self.login_url, self.true_user_login)
        access_token = 'Bearer  ' + res_login.data['data']['access_token']
        
        id = 1
        url = self.books_modifying_url + '?id=' + str(id)
        res = self.client.delete(url, headers={'authorization': access_token})
        self.assertEqual(res.status_code, 204)
        
        
        
