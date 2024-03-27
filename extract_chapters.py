# currently the extraction of chapters is done manually
# gpt api based automation did not work
# more research is needed to automate

import json

with open('config.json', 'r') as config_file:
    cfg = json.load(config_file)

os.environ['OPENAI_API_KEY'] = cfg['openai_api_key']
client = openai.OpenAI()

def extract_chapter_names(text):
    return invoke_llm("gpt3", data.prompt_extract_chapter_names, text)

path = cfg['processing_dir'] + "/" + pdf_name[:-4] + '_paginated_top_only.txt'
if not os.path.exists(path):
    pdf_text_top_only = pdf_text[:50000]
    open(path, 'w').write(pdf_text_top_only)
else:
    pdf_text_top_only = open(path, 'r').read()

