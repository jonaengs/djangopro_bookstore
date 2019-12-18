from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from users.forms import CustomUserCreationForm


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


class SignupPageTest(TestCase):
    username = 'username'
    email = 'user@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, "Sign up")
        self.assertNotContains(self.response, "This should not show")

    def test_signup_form(self):
        user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.first(), user)
        self.assertEqual(get_user_model().objects.first().username, user.username)
        self.assertEqual(get_user_model().objects.first().email, user.email)

