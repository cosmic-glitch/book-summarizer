import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from gen_chapter_metadata import gen_chapter_metadata
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

def extract_pages_from_pdf(pdf_path):
    assert os.path.exists(pdf_path)
    
    page_count = 1
    pages = []
    
    with open(pdf_path, 'rb') as file:
        for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
            text = extract_text(file, page_numbers=[page_count-1], laparams=LAParams())
            pages.append(text)
            page_count += 1
    
    return pages
    
def extract_items_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    items = []

    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            items.append(text)
    
    return items