from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'
        }

    def test_user_signup(self):
        data = {'username': 'newuser', 'password': 'strongpass123'}
        response = self.client.post('/api/signup/', data)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())

    def test_get_user_profile(self):
        response = self.client.get('/api/profile/', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json())

    def test_update_user_profile(self):
        data = {
            "username": "updated_user",
            "email": "updated@example.com",
            "first_name": "Updated",
            "password": "newpassword123",
            "last_name": "User"
        }
        response = self.client.put(
            '/api/profile/update/',
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        data = {'current_password': 'testpass123', 'new_password': 'newpass456'}
        response = self.client.put(
            '/api/password/change/',
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
