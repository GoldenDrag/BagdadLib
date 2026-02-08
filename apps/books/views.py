from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404


from .models import Book, Chapter
from .forms import UploadBookForm
from .utils import handle_book_upload


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
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, "detail.html", {"book": book})


def read(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    return render(request, "read.html", {"chapter": chapter})


def upload_book(request:HttpRequest):
    if request.method == "POST":
        form = UploadBookForm(request.POST, request.FILES)
        if form.is_valid():
            id = handle_book_upload(request.FILES["file"])
            return (HttpResponseRedirect(f"/{id}"))
    else:
        form = UploadBookForm()
    return render(request, "upload.html", {"form": form})