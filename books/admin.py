from django.contrib import admin
from django.contrib.admin import TabularInline

from books.models import Book, Review


class ReviewInline(TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ('title', 'author', 'price')


admin.site.register(Book, BookAdmin)
