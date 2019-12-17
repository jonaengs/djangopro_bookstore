from django.contrib.auth import get_user_model
from django.test import TestCase



class CustomUserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='user',
            email='user@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.email, 'user@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'superuser')
        self.assertEqual(user.email, 'superuser@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
