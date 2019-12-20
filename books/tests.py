from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from books.models import Book, Review


class BookTests(TestCase):
    username = 'reviewuser'
    password = 'password'
    email = 'reviewuser@email.com'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.special_permission = Permission.objects.get(codename='special_status')
        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00'
        )
        self.review = Review.objects.create(
            book=self.book,
            review='review text',
            author=self.user,
        )

    def test_book_listing(self):
        self.assertEqual(str(self.book.title), 'Harry Potter')
        self.assertEqual(str(self.book.author), 'JK Rowling')
        self.assertEqual(str(self.book.price), '25.00')

    def test_book_list_view_user_logged_in(self):
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % reverse('account_login'))
        response = self.client.get('%s?next=/books/' % reverse('account_login'))
        self.assertContains(response, 'Log in')

    def test_book_detail_view_with_permission(self):
        self.client.login(email=self.email, password=self.password)
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        no_response = self.client.get('/books/123456')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'review text')
        self.assertTemplateUsed(response, 'books/book_detail.html')
