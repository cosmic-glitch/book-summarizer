from extractors import extract_items_from_epub
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import re
import json
import os
import llm_prompts
import llm_api

cfg = json.load(open('config.json', 'r'))

def build_json_config_block(name, cover, author, affiliate_link, content_start_item, content_end_item):
    cfg_template = {          
                "name": name,
                "cover": f"<img src='{cover}' style='width:100px;height:auto;'>",
                "author": author,
                "affiliate_link": affiliate_link,
                "content_start_item": content_start_item,
                "content_end_item": content_end_item
        }
    return cfg_template

def infer_start_and_end(bkname):
    path = cfg['input_books_dir'] + bkname + ".epub"
    if os.path.exists(path):
        items = extract_items_from_epub(path)
        snippets = '\n\n'.join([f'Item {i}: {item[:200]}' for i, item in enumerate(items)])
        open('snippets_debug.txt', 'w').write(snippets)
        llm_output = llm_api.invoke("haiku", llm_prompts.extract_epub_content_boundaries, snippets)
        return re.findall(r'\d+', llm_output)

def get_amazon_links(name, author):
    options = Options()
    options.profile = FirefoxProfile(cfg['web_user_profile'])

    driver = webdriver.Firefox(options=options)

    driver.get("https://www.google.com")
    time.sleep(1)
    
    textarea = driver.find_element(By.NAME, "q")
    textarea.send_keys(f'amazon {name} {author}', Keys.ENTER)
    time.sleep(1)

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute('href')
        if href and "amazon.com" in href:
            href = href.split('?')[0]
            
            driver.get(href)
            time.sleep(1)
            cover = driver.find_element(By.ID, "landingImage").get_attribute('src')
            
            link = driver.find_element(By.XPATH, '//a[@title="Text"]')
            link.click()
            time.sleep(3)

            textarea = driver.find_element(By.ID, "amzn-ss-text-shortlink-textarea")
            affiliate_link = (textarea.text)

            body = driver.find_element(By.TAG_NAME, "body").text
            match = re.search(r"by ([^)]+) \(Author\)", body)
            assert match, "No author found"
            author = match.group(1)
            
            driver.quit()

            return cover, affiliate_link

    assert False, "Amazon link extraction failed"

def update_config(bkcfg):
    cfg['books'].append(bkcfg)
    json.dump(cfg, open('config.json', 'w'), indent=4)
