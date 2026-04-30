from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='Testpass123!'
        )
        self.client.login(username='testuser', password='Testpass123!')
        self.label = Label.objects.create(name='Bug')

    def test_label_list(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bug')

    def test_label_create(self):
        response = self.client.post(
            reverse('labels_create'), {'name': 'Feature'}
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='Feature').exists())

    def test_label_update(self):
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}),
            {'name': 'Critical'}
        )
        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Critical')

    def test_label_delete(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk})
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_protected(self):
        status = Status.objects.create(name='Новый')
        task = Task.objects.create(
            name='Test Task', status=status, author=self.user
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk})
        )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_labels_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('labels'))
        self.assertRedirects(response, '/login/?next=/labels/')
