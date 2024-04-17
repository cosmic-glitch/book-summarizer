# a utility script to capitalize the words in uppercase headings in HTML files.
# GPT3 sometimes outputs headings in uppercase, and this script can be used to capitalize the words in those headings.
# this hack is cheaper than regenerating the GPT3 output.

import os
import re

def capitalize_uppercase_words(text):
    def capitalize_match(match):
        words = match.group(1).split()
        return ' '.join(word.capitalize() for word in words)
    
    return re.sub(r'<h2>([A-Z\':\-\,? ]+)</h2>', lambda m: f'<h2>{capitalize_match(m)}</h2>', text)

# Define the directory where the files are located
output_directory = 'processing'

# Get a list of files in the directory
file_list = os.listdir(output_directory)

# Filter for HTML files if needed, or process all files
html_files = [file for file in file_list if file.endswith('.html')]

# Process each file
for html_file in html_files:
    file_path = os.path.join(output_directory, html_file)
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Transform the text
    transformed_text = capitalize_uppercase_words(text)

    # Write the transformed text back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(transformed_text)

print(f"Capitalization complete for {len(html_files)} files.")
