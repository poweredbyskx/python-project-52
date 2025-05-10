from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
