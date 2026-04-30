from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='Testpass123!'
        )
        self.client.login(username='testuser', password='Testpass123!')
        self.status = Status.objects.create(name='Новый')

    def test_status_list(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый')

    def test_status_create(self):
        response = self.client.post(
            reverse('statuses_create'), {'name': 'В работе'}
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='В работе').exists())

    def test_status_update(self):
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}),
            {'name': 'Завершен'}
        )
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Завершен')

    def test_status_delete(self):
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status.pk})
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('statuses'))
        self.assertRedirects(response, '/login/?next=/statuses/')
