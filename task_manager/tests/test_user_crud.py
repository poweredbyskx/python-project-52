from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserCreateTest(TestCase):
    def test_create_user(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

# Аналогично для обновления и удаления пользователей
