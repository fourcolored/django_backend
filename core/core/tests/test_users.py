from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser
from store.models import *

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "p4ssword123",
            "password2": "p4ssword123"
        }
    
    def test_register_user(self):
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login_user(self):
        self.client.post('/api/auth/register/', self.user_data)
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password1']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_user_invalid_credentials(self):
        login_data = {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
