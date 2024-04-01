# currently the extraction of chapters is done manually
# gpt api based automation did not work
# more research is needed to automate

import json
import llm_prompts as llm_prompts
import llm_api as llm_api
import os

# takes a book's config block as input, and produces a file with chapter metadata
def gen_chapter_metadata(bk):
    if os.path.exists(cfg['processing_dir'] + bk['name'] + '_chapters.txt'):
        return

    path = cfg['processing_dir'] + bk['name'] + '_paginated.txt'
    book = open(path, 'r').read()
    path = cfg['processing_dir'] + bk['name'] + '_paginated_short.txt'
    book_short = open(path, 'r').read()

    start_offset = book.find(f"<page {bk['toc_start']}>")
    end_offset = book.find(f"<page {bk['toc_end']+1}>")
    toc = book[start_offset:end_offset]

    start_offset = book_short.find(f"<page {bk['content_start']}>")
    end_offset = book_short.find(f"<page {bk['content_end']+1}>")
    body = book_short[start_offset:end_offset]

    text = f'TOC ->> {toc}\nBODY ->> {body}'
    chap_metadata = llm_api.invoke("gpt4", llm_prompts.extract_chapter_names, text)

    open(cfg['processing_dir'] + bk['name'] + '_chapters.txt', 'w').write(chap_metadata)

cfg = json.load(open('config.json', 'r'))
for bk in cfg['books']:
    print(f'Processing {bk["name"]}...')
    gen_chapter_metadata(bk)