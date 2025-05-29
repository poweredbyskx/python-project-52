import datetime
from django.test import TestCase, Client
from task_manager.users.models import User


class UserCRUDTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()

    def test_create(self):
        response = self.client.post(
            "/users/create/",
            {
                "first_name": "John",
                "last_name": "Smith",
                "username": "john",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="john").exists())
        user = User.objects.get(username="john")

        self.assertIsInstance(user.date_joined, datetime.datetime)
        self.assertTrue(user.check_password("testpass123"))
