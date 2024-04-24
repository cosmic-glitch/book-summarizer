# This script fully automates the generation of summaries for a new EPUB book.
# It takes the book name and author as input, searches on libgen, downloads the EPUB book, infers the content boundaries,
# fetches the cover image and affiliate link from Amazon, updates the book config block, and finally generates summaries.

import os
import json
from get_book import *
from gen_config import *
from gen_summaries import *

name = input("Enter the book name: ")
author = input("Enter the author: ")

cfg = json.load(open('config.json', 'r'))

if os.path.exists(cfg['input_books_dir'] + name + '.epub'):
    print('Book already downloaded. Skipping download...')
else:
    print('Searching for book...')
    while True:
        url = get_epub_url(name, author)
        print('Found book at:', url)
        choice = input('Download from this URL? yes/retry/override?: ').lower()
        if choice == 'y':
            download_book(name, url)
            print('Book downloaded')
            break
        elif choice == 'o':
            url = input('Enter ePUB URL: ')
            download_book(name, url)
            print('Book downloaded')
            break
        elif choice == 'r':
            print('Retrying...')
        else:
            assert False, 'Invalid choice'

content_start_item, content_end_item = infer_start_and_end(name)
print('Inferred content boundaries:', content_start_item, content_end_item)
if input('Want to override? [y/n]: ').lower() == 'y':
    content_start_item = input('Enter start item: ')
    content_end_item = input('Enter end item: ')

cover, affiliate_link = get_amazon_links(name, author)
print('Cover Image:', cover, '\nAffiliate Link:', affiliate_link)
if input('Want to override? [y/n]: ').lower() == 'y':
    cover = input('Enter cover image link: ')
    affiliate_link = input('Enter affiliate link: ')

theme = input('Enter the theme (will be automated soon): ')

cfg_blk = build_json_config_block(name, theme, cover, author, affiliate_link, content_start_item, content_end_item)
update_config(cfg_blk)
print('Config updated')

input('Press Enter to generate summaries...')
cfg = json.load(open('config.json', 'r'))
gen_summaries(cfg)