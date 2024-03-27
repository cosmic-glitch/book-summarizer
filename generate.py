import os
import openai
import data
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

input_dir = 'input'
processing_dir = 'processing'
output_dir = 'output'

os.environ['OPENAI_API_KEY'] = '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'
client = openai.OpenAI()

def invoke_llm(modelname, sysprompt, userprompt):
    completion = client.chat.completions.create(
        model=("gpt-4-0125-preview" if modelname=="gpt4" else "gpt-3.5-turbo-0125"),
        messages=[
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": userprompt}])
    return completion.choices[0].message.content
    
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

def extract_chapter_names(text):
    return invoke_llm("gpt4", data.prompt_extract_chapter_names, text)

def summarize_chapter(text):
    return invoke_llm("gpt3", data.prompt_summarize_chapter, text)

def summarize_book(pdf_name, cover_image):
    pdf_path = input_dir + "/" + pdf_name

    path = processing_dir + "/" + pdf_name[:-4] + '_paginated.txt'
    if not os.path.exists(path):
        pdf_text = extract_text_from_pdf(pdf_path)
        open(path, 'w').write(pdf_text)
    else:
        pdf_text = open(path, 'r').read()

    path = processing_dir + "/" + pdf_name[:-4] + '_paginated_top_only.txt'
    if not os.path.exists(path):
        pdf_text_top_only = pdf_text[:50000]
        open(path, 'w').write(pdf_text_top_only)
    else:
        pdf_text_top_only = open(path, 'r').read()

    path = processing_dir + "/" + pdf_name[:-4] + '_chapters.txt'
    if not os.path.exists(path):
        chapter_names = extract_chapter_names(pdf_text_top_only)
        open(path, 'w').write(chapter_names)
    else:
        chapter_names = open(path, 'r').read()

    chapters = chapter_names.split('\n')
    overall_summary = ''
    for c in chapters:
        chapN = c.split(',')

        print(chapN[0])
        path = processing_dir + "/" + pdf_name[:-4] + '_' + chapN[0] + '.txt'
        if not os.path.exists(path):
            start = pdf_text.find(f"<page{chapN[1]}>")
            end = pdf_text.find(f"<page{chapN[2]}>")
            assert(start > 0 and end > 0)
            chap_text = "Chapter Title-> " + chapN[0] + '\nChapter Body->\n' + pdf_text[start:end+1]
            open(path, 'w').write(chap_text)
        else:
            chap_text = open(path, 'r').read()

        path = processing_dir + "/" + pdf_name[:-4] + '_' + chapN[0] + '_summary.html'
        if not os.path.exists(path):
            chapN_summary = summarize_chapter(chap_text)
            open(path, 'w').write(chapN_summary)
        else:
            chapN_summary = open(path, 'r').read()

        overall_summary += chapN_summary

    overall_summary = f"<html><body><h1>Book Summary: {pdf_name[:-4]}</h1>{cover_image}" + overall_summary + "</body></html>"

    path = output_dir + "/" + pdf_name[:-4].replace(' ', '_') + '_summary.html'
    if not os.path.exists(path):
        open(path, 'w').write(overall_summary)
    else:
        overall_summary = open(path, 'r').read()

def main():
    toc = ''
    for book in data.book_list:
        summarize_book(book[0], book[1])
        toc += book[1] + f"<br><a href='{book[0][:-4].replace(' ', '_')}_summary.html'>{book[0][:-4]}</a><br><br>"
    toc = f"<html><body><h1>Book Summaries</h1>{toc}</body></html>"
    open(output_dir + "/index.html", 'w').write(toc)

main()