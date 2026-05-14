import pymupdf as fitz
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Book, Chapter, Paragraph
from .utils import _split_paragraphs, handle_book_upload


def _make_pdf(pages, toc=None):
    """ Create test pdf file """
    doc = fitz.open()
    for text in pages:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    if toc:
        doc.set_toc(toc)
    data = doc.tobytes()
    doc.close()
    return data


class SplitParagraphsTests(TestCase):
    """ Test split function """
    def test_splits_on_blank_lines(self):
        result = _split_paragraphs("one\n\ntwo\n\n\nthree")
        self.assertEqual(result, ["one", "two", "three"])

    def test_strips_and_drops_empty(self):
        result = _split_paragraphs("\n\n  hello  \n\n\n")
        self.assertEqual(result, ["hello"])


class HandleBookUploadTests(TestCase):
    """ Test book upload handler """
    def test_creates_book_with_chapters_from_toc(self):
        pdf = _make_pdf(
            ["Intro page text", "Body page text"],
            toc=[[1, "Intro", 1], [1, "Body", 2]],
        )
        upload = SimpleUploadedFile("mybook.pdf", pdf, 
                                    content_type="application/pdf")

        book_id = handle_book_upload(upload)

        book = Book.objects.get(pk=book_id)
        self.assertEqual(book.name, "mybook")
        names = list(book.chapter_set.order_by("pk").values_list("name", flat=True))
        self.assertEqual(names, ["Intro", "Body"])

    def test_no_toc_creates_single_chapter(self):
        pdf = _make_pdf(["Hello world content"])
        upload = SimpleUploadedFile("plain.pdf", pdf, content_type="application/pdf")

        book_id = handle_book_upload(upload)

        book = Book.objects.get(pk=book_id)
        self.assertEqual(book.chapter_set.count(), 1)
        self.assertEqual(book.chapter_set.first().name, "Chapter 1")

    def test_creates_paragraphs(self):
        pdf = _make_pdf(["alpha\n\nbeta\n\ngamma"])
        upload = SimpleUploadedFile("p.pdf", pdf, content_type="application/pdf")

        book_id = handle_book_upload(upload)

        chapter = Book.objects.get(pk=book_id).chapter_set.first()
        self.assertGreaterEqual(chapter.paragraph_set.count(), 1)
        self.assertTrue(Paragraph.objects.filter(chapter=chapter).exists())

    def test_dedupes_duplicate_chapter_names(self):
        pdf = _make_pdf(
            ["a", "b", "c"],
            toc=[[1, "Same", 1], [1, "Same", 2], [1, "Same", 3]],
        )
        upload = SimpleUploadedFile("dup.pdf", pdf, content_type="application/pdf")

        book_id = handle_book_upload(upload)

        names = set(Chapter.objects.filter(book_id=book_id).values_list("name", flat=True))
        self.assertEqual(len(names), 3)

    def test_returns_book_id_and_persists(self):
        pdf = _make_pdf(["text"])
        upload = SimpleUploadedFile("x.pdf", pdf, content_type="application/pdf")

        book_id = handle_book_upload(upload, name="Custom", description="desc")

        book = Book.objects.get(pk=book_id)
        self.assertEqual(book.name, "Custom")
        self.assertEqual(book.description, "desc")
