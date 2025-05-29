from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
import datetime


class StatusCRUDTest(TestCase):
    fixtures = ["statuses.json"]

    def setUp(self):
        self.client = Client()
        # Создаем и логиним пользователя, если нужно
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_create(self):
        response = self.client.post(reverse("statuses:create"), {"name": "новый1"})
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(name="новый1")
        self.assertIsInstance(status.created_at, datetime.datetime)
        # Если нужно, проверить timezone-aware:
        self.assertIsNotNone(status.created_at.tzinfo)

    def test_read(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
        status = Status.objects.get(name="новый1")
        self.assertIsInstance(status.created_at, datetime.datetime)

    def test_update(self):
        # Обновляем статус с id=2 из фикстуры
        response = self.client.post(
            reverse("statuses:update", args=[2]), {"name": "новый2"}
        )
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(pk=2)
        self.assertEqual(status.name, "новый2")
        self.assertIsInstance(status.created_at, datetime.datetime)
