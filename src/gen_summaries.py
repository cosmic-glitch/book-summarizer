import os
import llm_prompts
import llm_api
import json
import markdown
from extractors import extract_pages_from_pdf, extract_items_from_epub, extract_entire_html_from_epub
from gen_chapter_metadata import gen_chapter_metadata

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

def summarize_epub_book(html):
    return llm_api.invoke("gemini", llm_prompts.summarize_book, html)

def summarize_chapter(text):
    return llm_api.invoke("haiku@gcp", llm_prompts.summarize_chapter, text)
    
def shorten_summary(text):
    return llm_api.invoke("haiku@gcp", llm_prompts.shorten_summary, text)

def write_summary_to_html(cfg, bk, f_sum, f_shrt_sum, overall_summary):
    overall_summary = open(cfg['input_dir'] + 'summary_template.html', 'r').read().replace("$book_name$", bk['name']).replace("$book_summary$", bk['cover'] + overall_summary)
    open(f_sum, 'w').write(overall_summary)

    if not os.path.exists(f_shrt_sum):
        short_summary = shorten_summary(overall_summary)
        open(f_shrt_sum, 'w').write(short_summary)

# takes a book config block as input and generates the summary
def gen_summary_pdf(cfg, bk): 
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

    return overall_summary

# takes a book config block as input and generates the summary
def gen_summary_epub(cfg, bk):
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

    return overall_summary

# takes a book config block as input and generates the summary
def gen_summary_epub_one_shot(cfg, bk, f_sum):
    epub_path = cfg['input_books_dir'] + bk['name']  + '.epub'

    html = extract_entire_html_from_epub(epub_path)
    overall_summary = markdown.markdown(summarize_epub_book(html))

    return overall_summary

def gen_summaries(cfg):
    toc = ''

    for bk in cfg['books']:
        print(bk['name'])

        prefix = bk['name'].replace(' ', '_')
        f_sum = cfg['output_dir'] + prefix + '_summary.html'
        f_shrt_sum = cfg['output_dir'] + prefix + '_short_summary.html'
        f_book = cfg['input_books_dir'] + bk['name']
       
        if os.path.exists(f_sum) and os.path.exists(f_shrt_sum):
            print(f'\tSummary exists, skipping')
        else:
            if os.path.exists(f_book + '.pdf'):
                overall_summary = gen_summary_pdf(cfg, bk)
            elif os.path.exists(f_book + '.epub'):
                if 'summarize_whole_book' in bk and bk['summarize_whole_book'] == "True":
                    overall_summary = gen_summary_epub_one_shot(cfg, bk, f_sum)
                else:
                    overall_summary = gen_summary_epub(cfg, bk)
            else:
                assert False, f"Book {bk['name']} not found"

            write_summary_to_html(cfg, bk, f_sum, f_shrt_sum, overall_summary)

        # add book to index.html
        # hack - fix later by changing cover field to hold just plain URL
        cover_url = bk['cover'].split("src='")[1].split("'")[0]
        toc += f'\t\t{{ title: "{bk["name"]}", imageUrl: "{cover_url}", summary: "{prefix}_summary.html", short_summary: "{prefix}_short_summary.html", buy: "{bk["affiliate_link"]}", theme: "{bk["theme"]}" }},\n'

    toc = open(cfg['input_dir'] + 'index_template.html', 'r').read().replace('$placeholder$', toc)
    open(cfg['output_dir'] + 'index.html', 'w').write(toc)

if __name__ == '__main__':
    cfg = json.load(open('config.json', 'r'))
    gen_summaries(cfg)