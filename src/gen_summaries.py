import os
import llm_prompts
import llm_api
import json
from extractors import extract_pages_from_pdf, extract_items_from_epub
from gen_chapter_metadata import gen_chapter_metadata

cfg = json.load(open('config.json', 'r'))

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
    return llm_api.invoke("gpt3", llm_prompts.shorten_summary, text)

def write_summary_to_html(bk, overall_summary):
    overall_summary = open(cfg['input_dir'] + 'summary_template.html', 'r').read().replace("$book_name$", bk['name']).replace("$book_summary$", bk['cover'] + overall_summary)
    path = cfg['output_dir'] + bk['name'].replace(' ', '_') + '_summary.html'
    open(path, 'w').write(overall_summary)

    path = cfg['output_dir'] + bk['name'].replace(' ', '_') + '_short_summary.html'
    if not os.path.exists(path):
        short_summary = shorten_summary(overall_summary)
        open(path, 'w').write(short_summary)

# takes a book config block as input and generates the summary
def gen_summary_pdf(bk): 
    print(bk['name'])

    path = cfg['processing_dir'] + bk['name']  + '_paginated.txt'
    path_short = cfg['processing_dir'] + bk['name']  + '_paginated_short.txt'
    if not os.path.exists(path) or not os.path.exists(path_short):
        pages = extract_pages_from_pdf(cfg['input_books_dir'] + bk['name'] + '.pdf')
        pdf_text = '\n'.join(f'<page {i}>\n{page}' for i, page in enumerate(pages, start=1))
        pdf_text_short = '\n'.join(f'<page {i}>\n{page[:100]}' for i, page in enumerate(pages, start=1))
        open(path, 'w').write(pdf_text)
        open(path_short, 'w').write(pdf_text_short)
    else:
        pdf_text = open(path, 'r').read()
        pdf_text_short = open(path_short, 'r').read()

    path = cfg['processing_dir'] + bk['name'] + '_chapters.txt'
    if not os.path.exists(path):
        gen_chapter_metadata(bk)
    chapter_names = open(path, 'r').read()
    validate_chapter_names(chapter_names)

    chapters = chapter_names.split('\n')
    overall_summary = ''
    for c in chapters:
        chapN = c.split(';')

        print('\t' + chapN[0])
        path = cfg['processing_dir'] + bk['name'] + '_' + chapN[0] + '.txt'
        if not os.path.exists(path):
            start = pdf_text.find(f"<page{chapN[1]}>")
            end = pdf_text.find(f"<page {int(chapN[2])+1}>")
            assert(start > 0 and end > 0)
            chap_text = "Chapter Title-> " + chapN[0] + '\nChapter Body->\n' + pdf_text[start:end]
            open(path, 'w').write(chap_text)
        else:
            chap_text = open(path, 'r').read()

        path = cfg['processing_dir'] + bk['name'] + '_' + chapN[0] + '_summary.html'
        if not os.path.exists(path):
            chapN_summary = summarize_chapter(chap_text)
            open(path, 'w').write(chapN_summary)
        else:
            chapN_summary = open(path, 'r').read()

        overall_summary += chapN_summary

    write_summary_to_html(bk, overall_summary)

# takes a book config block as input and generates the summary
def gen_summary_epub(bk):
    print(bk['name'])

    path = cfg['input_books_dir'] + bk['name']  + '.epub'
    items = extract_items_from_epub(path)
    items = items[int(bk['content_start_item']):int(bk['content_end_item'])+1]

    overall_summary = ''
    for i, item in enumerate(items, start=1):
        print(f'\tItem {i}')

        if len(item) < 200:
            print(f'\t\tItem {i} too short, skipping')
            continue
        
        path = cfg['processing_dir'] + bk['name'] + f'_item {i}.txt'
        if not os.path.exists(path):
            open(path, 'w').write(item)
        else:
            item = open(path, 'r').read()

        path = cfg['processing_dir'] + bk['name'] + f'_item {i}_summary.html'
        if not os.path.exists(path):
            item_summary = summarize_chapter(item)
            open(path, 'w').write(item_summary)
        else:
            item_summary = open(path, 'r').read()

        overall_summary += item_summary

    write_summary_to_html(bk, overall_summary)

def gen_summaries():
    toc = ''

    for bk in cfg['books']:
        if os.path.exists(cfg['input_books_dir'] + bk['name'] + '.pdf'):
            gen_summary_pdf(bk)
        elif os.path.exists(cfg['input_books_dir'] + bk['name'] + '.epub'):
            gen_summary_epub(bk)
        else:
            assert False, f"Book {bk['name']} not found"

        bk_prefix = bk['name'].replace(' ', '_')

        # add book to index.html
        toc += f"""<div class="book">
            <div class="book-title">{bk['name']}</div>
            {bk['cover']}
            <div class="book-links">
                <a href="{bk_prefix}_short_summary.html">Short Summary</a>
                <a href="{bk_prefix}_summary.html">Chapter-level Summary</a>
                <a href='{bk['affiliate_link']}'>Buy On Amazon</a>
            </div>
        </div>"""
    
    toc = open(cfg['input_dir'] + 'index_template.html', 'r').read().replace('$placeholder$', toc)
    open(cfg['output_dir'] + 'index.html', 'w').write(toc)

if __name__ == '__main__':
    gen_summaries()