from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Book


def index(request):
    books = Book.objects.order_by("-created_at")[:5]
    template = loader.get_template("index.html")
    context = {"books": books}
    return HttpResponse(template.render(context, request))


def latest(request):
    latest_updated_books = Book.objects.order_by("-updated_at")[:10]
    context = {"books": latest_updated_books}
    return render(request, "latest.html", context)


def detail(request, book_id):
    try:
        book = Book.objects.get(pkl=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, "detail.html", {"book": book})


def read(request, chapter_id):
    return HttpResponse(f"Here is contents of a chapter {chapter_id}")