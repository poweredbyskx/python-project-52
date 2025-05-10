from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserListViewTest(TestCase):
    def test_user_list_view(self):
        # Тестируем, что страница пользователей доступна
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/users/list.html')

# Другие тесты для других страниц (create, update, delete) можно добавить здесь.
