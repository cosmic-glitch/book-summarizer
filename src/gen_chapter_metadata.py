# currently the extraction of chapters is done manually
# gpt api based automation did not work
# more research is needed to automate

import json
import src.llm_prompts as llm_prompts
import src.llm_api as llm_api

cfg = json.load(open('config.json', 'r'))

def extract_chapter_names(text):
    return llm_api.invoke("haiku", llm_prompts.extract_chapter_names, text)

def main():    
    path = cfg['processing_dir'] + "/Elon Musk_paginated.txt"
    book = open(path, 'r').read()
    toc_start = 627
    toc_end = 637
    start_offset = book.find(f"<page {toc_start}>")
    end_offset = book.find(f"<page {toc_end+1}>")
    print(extract_chapter_names(book[start_offset:end_offset]))
    
main()