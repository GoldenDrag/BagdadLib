from django.shortcuts import render
from django.http import HttpResponse

from .models import Book


def index(request):
    books = Book.objects[:5]
    result = (", ").join([book.name for book in books])
    return HttpResponse(f"Here are our top books: {result}")


def latest(request):
    latest_updated_books = Book.objects.order_by("-updated_at")[:10]
    result = (", ").join([book.name for book in latest_updated_books])
    return HttpResponse(f"Here is latest updated works: {result}")


def detail(request, book_id):
    return HttpResponse(f"Here is info about {book_id}")


def read(request, chapter_id):
    return HttpResponse(f"Here is contents of a chapter {chapter_id}")