from django.test import TestCase, Client
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User

class TasksCRUDTest(TestCase):
    fixtures = ['tasks.json']  # Если у тебя есть фикстура tasks.json с тестовыми данными

    def setUp(self):
        self.client = Client()
        # Создаем тестового пользователя и логинимся
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create(self):
        # Используем reverse для получения URL
        url = reverse('tasks:create')  # или укажи правильный неймспейс и имя url
        response = self.client.post(url, {'name': 'tota', 'status': 1})
        # Проверяем, что редирект (создание прошло успешно)
        self.assertEqual(response.status_code, 302)

        # Проверяем, что задача создалась и у неё статус с id=1 (статус с id=6 не обязателен)
        task = Task.objects.get(name="tota")
        self.assertEqual(task.status.id, 1)

    def test_read(self):
        url = reverse('tasks:list')  # или укажи правильный url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Теперь 200, а не 302

        # Проверим, что в базе есть задача с именем из фикстуры
        task = Task.objects.get(name="tota")
        self.assertIsNotNone(task)

    def test_read_filters(self):
        url = reverse('tasks:list')
        response = self.client.get(url, {'status': 6})
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.filter(status_id=6)
        self.assertTrue(tasks.exists())
