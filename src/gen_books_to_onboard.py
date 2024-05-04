import json
import llm_api
import llm_prompts

cfg = json.load(open('config.json', 'r'))

books = cfg['books']

onboarded_books = ''
for book in books:
    onboarded_books += f"{book['name']} by {book['author']}\n"

proposed_books = llm_api.invoke("gpt4", llm_prompts.books_to_onboard, onboarded_books)

print(proposed_books)