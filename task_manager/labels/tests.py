from django.test import TestCase, Client
from django.urls import reverse
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class LabelsCRUDTest(TestCase):
    fixtures = ["labels.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

    def test_create(self):
        url = reverse("labels:create")
        response = self.client.post(url, {"name": "bug1"})
        self.assertEqual(response.status_code, 302)
        label = Label.objects.get(name="bug1")
        self.assertEqual(label.name, "bug1")

    def test_read(self):
        url = reverse("labels:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        label = Label.objects.get(name="bug1")
        self.assertEqual(label.id, 3)

    def test_delete(self):
        url = reverse("labels:delete", args=[3])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=3)
