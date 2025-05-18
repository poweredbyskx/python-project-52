from django.test import TestCase, Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User

class TasksCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Создаем статус для тестов
        self.status1 = Status.objects.create(name='Status 1')
        self.status6 = Status.objects.create(name='Status 6')

        # Создаем задачу для чтения
        self.task = Task.objects.create(name='tota', status=self.status1, author=self.user)

    def test_create(self):
        url = reverse('tasks:create')
        response = self.client.post(url, {'name': 'new task', 'status': self.status1.id})
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(name='new task')
        self.assertEqual(task.status, self.status1)

    def test_read(self):
        url = reverse('tasks:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        task = Task.objects.get(name='tota')
        self.assertIsNotNone(task)

    def test_read_filters(self):
        url = reverse('tasks:list')
        response = self.client.get(url, {'status': self.status6.id})
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.filter(status=self.status6)
        self.assertTrue(tasks.exists())
