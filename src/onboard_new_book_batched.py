# This script fully automates the generation of summaries for a new EPUB book.
# It takes the book name and author as input, searches on libgen, downloads the EPUB book, infers the content boundaries,
# fetches the cover image and affiliate link from Amazon, updates the book config block, and finally generates summaries.

import os
import json
from get_book import *
from gen_config import *
from gen_summaries import *

books = [
   {"name": "Structure and Interpretation of Computer Programs", "author": "Harold Abelson and Gerald Jay Sussman", "theme": "Technology"}
]

for book in books:
    name, author, theme = book["name"], book["author"], book["theme"]

    cfg = json.load(open('config.json', 'r'))

    try:
        print('Processing book:', name)

        if os.path.exists(cfg['input_books_dir'] + name + '.epub'):
            print('Book already downloaded. Skipping download...')
        else:
            print('Searching for book...')
            url = get_epub_url(name, author)
            print('Found book at:', url)
            download_book(name, url)
            
        if any(book['name'] == name for book in cfg['books']):
            print('Book already exists in config. Skipping config update...')
        else:
            cover, affiliate_link = get_amazon_links(name, author)
            print('Cover Image:', cover, '\nAffiliate Link:', affiliate_link)

            cfg_blk = build_json_config_block(name, theme, cover, author, affiliate_link)
            update_config(cfg_blk)
            print('Config updated')

    except Exception as e:
        print(f"Error processing book {name}: {e}. Skipping...")
        continue

cfg = json.load(open('config.json', 'r'))
gen_summaries(cfg)