
# Book Summary Generator

## Description

This Python project automates the generation of summaries for books available in PDF and EPUB formats. It extracts text from these files, divides the content into manageable sections or chapters, and uses LLMs via an API to generate both detailed and concise summaries. The final summaries are saved as HTML files which can be viewed in a web browser.

## Features

- **PDF and EPUB Support**: Process books in PDF and EPUB file formats.
- **Automatic Text Extraction**: Extract text using PDFMiner for PDF files and BeautifulSoup for EPUB files.
- **Chapter Summarization**: Automatically generate summaries for each chapter or section.
- **Content Validation**: Ensure chapter metadata is correctly formatted and content is extracted properly.
- **Interactive Summaries**: Output summaries are saved as HTML files, which include links to purchase the books.

## Prerequisites

- Python 3.8+
- Libraries: pdfminer.six, ebooklib, BeautifulSoup4
- Configuration: A JSON file named `config.json` that includes paths and API credentials.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/cosmic-glitch/book-summarizer.git
   ```
2. Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```
3. Ensure you have a valid `config.json` in the project root with the necessary configurations.

## Configuration

The `config.json` file should include the following keys:
- `input_books_dir`: Directory containing the book files.
- `processing_dir`: Directory for storing intermediate processing files.
- `output_dir`: Directory where the summary HTML files will be saved.
- `books`: A list of books to process, specifying file names and other metadata.

See config.json for examples.

## Usage

Run the script to start processing books specified in the `config.json` file:
```
python gen_summaries.py
```

The summaries will be generated in the `output_dir` specified, with links to detailed and short summaries for each book

## License

[MIT](https://choosealicense.com/licenses/mit/)
