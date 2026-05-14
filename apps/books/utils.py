import re

import pymupdf as fitz
from django.db import transaction

from .models import Book, Chapter, Paragraph


def _read_bytes(file):
    if hasattr(file, "seek"):
        file.seek(0)
    return file.read() if hasattr(file, "read") else file


def _split_paragraphs(text):
    parts = re.split(r"\n\s*\n+", text)
    return [p.strip() for p in parts if p.strip()]


def _extract_chapters(doc):
    toc = doc.get_toc()
    top = [t for t in toc if t[0] == 1] if toc else []
    if not top:
        text = "".join(doc.load_page(p).get_text() 
                       for p in range(doc.page_count))
        return [("Chapter 1", text)]

    chapters = []
    for i, (_, title, start) in enumerate(top):
        end = top[i + 1][2] - 1 if i + 1 < len(top) else doc.page_count
        text = "".join(doc.load_page(p).get_text() 
                       for p in range(start - 1, end))
        chapters.append((title, text))
    return chapters


def _unique_name(name, used):
    base = name[:64] or "Chapter"
    candidate = base
    n = 2
    while candidate in used:
        suffix = f" ({n})"
        candidate = base[: 64 - len(suffix)] + suffix
        n += 1
    used.add(candidate)
    return candidate


@transaction.atomic
def handle_book_upload(file, name=None, description=""):
    data = _read_bytes(file)
    doc = fitz.open(stream=data, filetype="pdf")
    try:
        book_name = name or getattr(file, "name","Untitled").rsplit(".", 1)[0]
        book = Book.objects.create(name=book_name[:64], 
                                   description=description)
        used = set()
        for chapter_name, chapter_text in _extract_chapters(doc):
            chapter = Chapter.objects.create(
                book=book,
                name=_unique_name(chapter_name, used),
                raw_content={"text": chapter_text},
            )
            for para in _split_paragraphs(chapter_text):
                Paragraph.objects.create(chapter=chapter, 
                                         content=para)
        return book.id
    finally:
        doc.close()
