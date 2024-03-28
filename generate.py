import os
import openai
import data
import llm
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import json

cfg = json.load(open('config.json', 'r'))
    
def extract_text_from_pdf(pdf_path):
    print(pdf_path)
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
        print(line)
        assert len(flds) == 3
        assert int(flds[2]) - int(flds[1]) >= 1 and int(flds[2]) - int(flds[1]) < 50
        assert int(flds[1]) > prev
        prev = int(flds[1])

def summarize_chapter(text):
    return llm.invoke_llm("gpt3", data.prompt_summarize_chapter, text)

def summarize_book(pdf_name, cover_image):
    pdf_path = cfg['input_books_dir'] + "/" + pdf_name

    path = cfg['processing_dir'] + "/" + pdf_name[:-4] + '_paginated.txt'
    if not os.path.exists(path):
        pdf_text = extract_text_from_pdf(pdf_path)
        open(path, 'w').write(pdf_text)
    else:
        pdf_text = open(path, 'r').read()

    path = cfg['input_dir'] + "/" + pdf_name[:-4] + '_chapters.txt'
    assert os.path.exists(path)
    chapter_names = open(path, 'r').read()
    validate_chapter_names(chapter_names)

    chapters = chapter_names.split('\n')
    overall_summary = ''
    for c in chapters:
        chapN = c.split(';')

        print(chapN[0])
        path = cfg['processing_dir'] + "/" + pdf_name[:-4] + '_' + chapN[0] + '.txt'
        if not os.path.exists(path):
            start = pdf_text.find(f"<page{chapN[1]}>")
            end = pdf_text.find(f"<page{chapN[2]}>")
            assert(start > 0 and end > 0)
            chap_text = "Chapter Title-> " + chapN[0] + '\nChapter Body->\n' + pdf_text[start:end+1]
            open(path, 'w').write(chap_text)
        else:
            chap_text = open(path, 'r').read()

        path = cfg['processing_dir'] + "/" + pdf_name[:-4] + '_' + chapN[0] + '_summary.html'
        if not os.path.exists(path):
            chapN_summary = summarize_chapter(chap_text)
            open(path, 'w').write(chapN_summary)
        else:
            chapN_summary = open(path, 'r').read()

        overall_summary += chapN_summary

    overall_summary = f"<html><body><h1>Book Summary: {pdf_name[:-4]}</h1>{cover_image}" + overall_summary + "</body></html>"

    path = cfg['output_dir'] + "/" + pdf_name[:-4].replace(' ', '_') + '_summary.html'
    if not os.path.exists(path):
        open(path, 'w').write(overall_summary)
    else:
        overall_summary = open(path, 'r').read()

def main():
    toc = ''
    for book in data.book_list:
        summarize_book(book[0], book[1])
        toc += f"""<div class="book">
                        {book[1].replace('200px', '100px')}
                        <a href='{book[0][:-4].replace(' ', '_')}_summary.html'>{book[0][:-4]}</a>
                    </div>\n"""
        
        f"""<div class="book">
            {book[1].replace('200px', '100px')}
            <div>{book[2]}</div>
            <a href='{book[0][:-4].replace(' ', '_')}_short_summary.html'>Short Summary</a>
            <a href='{book[0][:-4].replace(' ', '_')}_summary.html'>Chapter Summary</a>
            <a href='#purchase-link'>Purchase</a>
        </div>"""
    toc = open(cfg['input_dir'] + "/index_experimental.html", 'r').read().replace("$placeholder$", toc)
    open(cfg['output_dir'] + "/index.html", 'w').write(toc)

main()