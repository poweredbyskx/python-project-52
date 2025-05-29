from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
import datetime


class StatusCRUDTest(TestCase):
    fixtures = ["statuses.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.client.login(username="testuser", password="12345")

    def test_create(self):
        response = self.client.post(
            reverse("statuses:create"),
            {"name": "новый1"},
        )
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(name="новый1")
        self.assertIsInstance(status.created_at, datetime.datetime)
        self.assertIsNotNone(status.created_at.tzinfo)

    def test_read(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
