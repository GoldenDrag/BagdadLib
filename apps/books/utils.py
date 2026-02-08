import pathlib
import pymupdf4llm as pdf_processer

def handle_book_upload(file):
    # passing an object with no path -> causing an error
    markdown = pdf_processer.to_markdown(file)
    text = pdf_processer.to_text(file)

    pathlib.Path("output.md").write_bytes(markdown.encode())
    pathlib.Path("output.txt").write_bytes(text.encode())

