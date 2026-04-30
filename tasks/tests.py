from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='Testpass123!'
        )
        self.other_user = User.objects.create_user(
            username='other', password='Testpass123!'
        )
        self.status = Status.objects.create(name='Новый')
        self.client.login(username='testuser', password='Testpass123!')
        self.task = Task.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user,
        )

    def test_task_list(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create(self):
        response = self.client.post(reverse('tasks_create'), {
            'name': 'New Task',
            'status': self.status.pk,
        })
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update(self):
        response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.pk}),
            {'name': 'Updated Task', 'status': self.status.pk}
        )
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_by_author(self):
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk})
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author(self):
        self.client.login(username='other', password='Testpass123!')
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk})
        )
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks'))
        self.assertRedirects(response, '/login/?next=/tasks/')


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='Testpass123!'
        )
        self.other_user = User.objects.create_user(
            username='other', password='Testpass123!'
        )
        self.status1 = Status.objects.create(name='Новый')
        self.status2 = Status.objects.create(name='В работе')
        self.label = Label.objects.create(name='Bug')
        self.client.login(username='testuser', password='Testpass123!')
        self.task1 = Task.objects.create(
            name='My Task', status=self.status1, author=self.user,
            executor=self.user,
        )
        self.task2 = Task.objects.create(
            name='Other Task', status=self.status2,
            author=self.other_user,
        )
        self.task1.labels.add(self.label)

    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks'), {'status': self.status1.pk}
        )
        self.assertContains(response, 'My Task')
        self.assertNotContains(response, 'Other Task')

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse('tasks'), {'executor': self.user.pk}
        )
        self.assertContains(response, 'My Task')
        self.assertNotContains(response, 'Other Task')

    def test_filter_by_label(self):
        response = self.client.get(
            reverse('tasks'), {'labels': self.label.pk}
        )
        self.assertContains(response, 'My Task')
        self.assertNotContains(response, 'Other Task')

    def test_filter_self_tasks(self):
        response = self.client.get(
            reverse('tasks'), {'self_tasks': 'on'}
        )
        self.assertContains(response, 'My Task')
        self.assertNotContains(response, 'Other Task')
