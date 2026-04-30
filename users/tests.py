from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCreateTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('users_create'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'Complexpass123!',
            'password2': 'Complexpass123!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_invalid(self):
        response = self.client.post(reverse('users_create'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password1': 'pass',
            'password2': 'different',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())


class UserUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!',
            first_name='Test',
            last_name='User',
        )
        self.client.login(username='testuser', password='Testpass123!')

    def test_update_user(self):
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user.pk}),
            {
                'first_name': 'Updated',
                'last_name': 'User',
                'username': 'testuser',
                'password1': 'Newpass123!',
                'password2': 'Newpass123!',
            }
        )
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_update_other_user_forbidden(self):
        other = User.objects.create_user(
            username='other', password='Otherpass123!',
            first_name='Other', last_name='User',
        )
        response = self.client.post(
            reverse('users_update', kwargs={'pk': other.pk}),
            {
                'first_name': 'Hacked',
                'last_name': 'User',
                'username': 'other',
                'password1': 'Newpass123!',
                'password2': 'Newpass123!',
            }
        )
        self.assertRedirects(response, reverse('users'))
        other.refresh_from_db()
        self.assertEqual(other.first_name, 'Other')


class UserDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='Testpass123!',
            first_name='Test',
            last_name='User',
        )
        self.client.login(username='testuser', password='Testpass123!')

    def test_delete_user(self):
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user.pk})
        )
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_delete_other_user_forbidden(self):
        other = User.objects.create_user(
            username='other', password='Otherpass123!',
        )
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': other.pk})
        )
        self.assertRedirects(response, reverse('users'))
        self.assertTrue(User.objects.filter(pk=other.pk).exists())
