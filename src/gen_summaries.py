import os
import llm_prompts
import llm_api
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import json

cfg = json.load(open('config.json', 'r'))
    
def extract_text_from_pdf(pdf_path):
    assert os.path.exists(pdf_path)
    
    extracted_text = ""  # Initialize the string to accumulate text
    page_count = 1       # Initialize page counter
    
    with open(pdf_path, 'rb') as file:
        for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
            text = extract_text(file, page_numbers=[page_count-1], laparams=LAParams())
            extracted_text += f"<page {page_count}>\n{text}\n"
            page_count += 1
    
    return extracted_text.replace('\t', ' ')

def validate_chapter_names(chapter_names):
    assert len(chapter_names) > 0
    assert len(chapter_names.split('\n')) > 1

    prev = 0
    for line in chapter_names.split('\n'):
        flds = line.split(';')
        assert len(flds) == 3
        assert int(flds[2]) - int(flds[1]) >= 1 and int(flds[2]) - int(flds[1]) < 50
        assert int(flds[1]) > prev
        prev = int(flds[1])

def summarize_chapter(text):
    return llm_api.invoke("gpt3", llm_prompts.summarize_chapter, text)

def shorten_summary(text):
    return llm_api.invoke("opus", llm_prompts.shorten_summary, text)

def gen_summary(book_name, cover_image):
    print(book_name)
    pdf_path = cfg['input_books_dir'] + "/" + book_name + '.pdf'

    path = cfg['processing_dir'] + "/" + book_name + '_paginated.txt'
    if not os.path.exists(path):
        pdf_text = extract_text_from_pdf(pdf_path)
        open(path, 'w').write(pdf_text)
    else:
        pdf_text = open(path, 'r').read()

    path = cfg['input_dir'] + "/" + book_name + '_chapters.txt'
    assert os.path.exists(path)
    chapter_names = open(path, 'r').read()
    validate_chapter_names(chapter_names)

    chapters = chapter_names.split('\n')
    overall_summary = ''
    for c in chapters:
        chapN = c.split(';')

        print('\t' + chapN[0])
        path = cfg['processing_dir'] + "/" + book_name + '_' + chapN[0] + '.txt'
        if not os.path.exists(path):
            start = pdf_text.find(f"<page{chapN[1]}>")
            end = pdf_text.find(f"<page {int(chapN[2])+1}>")
            assert(start > 0 and end > 0)
            chap_text = "Chapter Title-> " + chapN[0] + '\nChapter Body->\n' + pdf_text[start:end]
            open(path, 'w').write(chap_text)
        else:
            chap_text = open(path, 'r').read()

        path = cfg['processing_dir'] + "/" + book_name + '_' + chapN[0] + '_summary.html'
        if not os.path.exists(path):
            chapN_summary = summarize_chapter(chap_text)
            open(path, 'w').write(chapN_summary)
        else:
            chapN_summary = open(path, 'r').read()

        overall_summary += chapN_summary

    overall_summary = f"<html><body><h1>Book Summary: {book_name}</h1>{cover_image}" + overall_summary + "</body></html>"
    path = cfg['output_dir'] + "/" + book_name.replace(' ', '_') + '_summary.html'
    open(path, 'w').write(overall_summary)

    path = cfg['output_dir'] + "/" + book_name.replace(' ', '_') + '_short_summary.html'
    if not os.path.exists(path):
        short_summary = shorten_summary(overall_summary)
        open(path, 'w').write(short_summary)

def main():
    toc = ''

    for bk in cfg['books']:
        gen_summary(bk['name'], bk['cover'].replace('100px', '200px'))

        bk_prefix = bk['name'].replace(' ', '_')

        # add book to index.html
        toc += f"""<div class="book">
            {bk['cover']}
            <div>{bk['author']}</div>
            <a href='{bk_prefix}_short_summary.html'>5 minute Summary</a>
            <a href='{bk_prefix}_summary.html'>30 min Summary</a>
            <a href='{bk['affiliate_link']}'>Buy On Amazon</a>
        </div>"""
    
    toc = open(cfg['input_dir'] + "/index_template.html", 'r').read().replace("$placeholder$", toc)
    open(cfg['output_dir'] + "/index.html", 'w').write(toc)

main()