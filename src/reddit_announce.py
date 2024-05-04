import json

def find_book_index(books, book_name):
    return next((index for index, book in enumerate(books) if book['name'] == book_name), -1)

cfg = json.load(open('config.json', 'r'))

books = cfg['books']

last_onboarded = 'The Upanishads'
index = find_book_index(books, last_onboarded)

print(f"{len(books)-index-1} books addded on 3rd May 2024:\n")
for i in range(index + 1, len(books)):
    url = f"www.booksummary.pro/{books[i]['name'].replace(' ', '_')}_summary.html"
    print(f"**{books[i]['name']}** by {books[i]['author']} - {url}")
    print()