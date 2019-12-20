from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BookTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00'
        )

    def test_book_listing(self):
        self.assertEqual(str(self.book.title), 'Harry Potter')
        self.assertEqual(str(self.book.author), 'JK Rowling')
        self.assertEqual(str(self.book.price), '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        no_response = self.client.get(reverse('book_detail', args='123456'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 400)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_detail.html')
