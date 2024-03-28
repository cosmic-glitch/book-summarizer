# currently the extraction of chapters is done manually
# gpt api based automation did not work
# more research is needed to automate

import json
import openai
import data
import os
import llm

cfg = json.load(open('config.json', 'r'))

def extract_chapter_names(text):
    return llm.invoke_llm("opus", data.prompt_extract_chapter_names, text)

def main():
    path = cfg['processing_dir'] + "/Elon Musk_paginated.txt"
    top_bytes = open(path, 'r').read()[100000:150000]
    print(extract_chapter_names(top_bytes))
    
main()