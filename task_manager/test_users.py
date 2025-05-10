from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCRUDTest(TestCase):
    def test_create_user(self):
        response = self.client.post(reverse('users_create'), {
            'username': 'samvel',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='samvel').exists())
