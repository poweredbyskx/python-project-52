from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Label, Task, Status

from django.test import TestCase
from django.urls import reverse
from .models import Task, User, Label

class TaskFilterTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.label = Label.objects.create(name='Bug')
        self.task1 = Task.objects.create(
            title='Test Task 1',
            status='Open',
            assignee=self.user,
            author=self.user
        )
        self.task2 = Task.objects.create(
            title='Test Task 2',
            status='Closed',
            assignee=self.user,
            author=self.user
        )
        self.task1.labels.add(self.label)

    def test_filter_by_status(self):
        response = self.client.get(reverse('task_list') + '?status=Open')
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_filter_by_assignee(self):
        response = self.client.get(reverse('task_list') + '?assignee=' + str(self.user.id))
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')

    def test_filter_by_label(self):
        response = self.client.get(reverse('task_list') + '?labels=' + str(self.label.id))
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_filter_by_author(self):
        response = self.client.get(reverse('task_list') + '?author=' + str(self.user.id))
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')

class LabelTests(TestCase):

    def test_create_label(self):
        response = self.client.post(reverse('label_create'), {'name': 'Bug'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Bug').exists())

class StatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.status = Status.objects.create(name='Новый статус')

    def test_status_list(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый статус')

    def test_create_status(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('status_create'), {'name': 'В работе'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 2)

    def test_update_status(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('status_update', args=[self.status.pk]), {'name': 'На тестировании'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'На тестировании')

    def test_delete_status(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)

class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.status = Status.objects.create(name='новый')

    def test_task_creation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_create'), {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirection after successful creation
        self.assertEqual(Task.objects.count(), 1)
