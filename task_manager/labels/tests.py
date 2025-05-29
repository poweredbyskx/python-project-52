from django.test import TestCase, Client
from django.urls import reverse
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class LabelsCRUDTest(TestCase):
    fixtures = ["labels.json"]

    def setUp(self):
        self.client = Client()
        # Создаем пользователя и логинимся
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_create(self):
        url = reverse("labels:create")  # исправь на реальный неймспейс
        response = self.client.post(url, {"name": "bug1"})
        self.assertEqual(response.status_code, 302)
        label = Label.objects.get(name="bug1")
        self.assertEqual(label.name, "bug1")

    def test_read(self):
        url = reverse("labels:list")  # исправь на правильный url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        label = Label.objects.get(name="bug1")
        self.assertEqual(label.id, 3)  # Убедись, что в фикстуре есть id=3 и имя bug1

    def test_delete(self):
        url = reverse("labels:delete", args=[3])  # проверь url и id из фикстуры
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Обычно после удаления редирект

        # Проверяем, что метка удалена
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=3)
