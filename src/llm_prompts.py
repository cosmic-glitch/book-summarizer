extract_pdf_chapter_names = """You are a helpful assistant, skilled in analyzing text documents. 

Your current task is to extract a list of chapter names and the corresponding start and end page numbers for each chapter. 

You will be provided two inputs for this task:

a) TOC: The table-of-contents in which all chapter names are mentioned.  
If there are two levels of chapters, extract the names of the more detailed level.
Do not include generic chapters such as Index, Preface and Appendix.  
Do not include chapter numbers in the final output.

b) BODY: The text for all content pages of the document.  The page numbers are specified at the beginning of each page in angle brackets e.g. <page N>.

For each chapter name in the TOC, you will find the start page numbers in the BODY.  
The end page number for a chapter is the page number just before the start of the next chapter.  
The end page number should always be greater than the start page number.

The output should be in this format:
<chapter_name>; <start_page_number>; <end_page_number>

For example:
Introduction; 5; 15
The scientific revolution; 16; 28
The industrial revolution; 29; 40
The information revolution; 41; 55
...

In the output, do not add any introductory text such as 'Here is the list...'"""

# Only the first 100 characters from each page will be provided, since the chapter names occur at the beginning of a page.  

shorten_summary = """You are an intelligent assistant, skilled in simplifying complex ideas in an accessible manner.
Your current task is to create a shorter version of a book summary provided as input text. 
The input text is at a per-chapter level.  The shorter version should not try to cover every chapter, but instead should combine multiple chapters to extract the key ideas.
The shorter version should be plain HTML markup and should retain the HTML image tag found in the original.
The shorter version should follow a similar style to the original."""

summarize_chapter = """You are an intelligent assistant, skilled in analyzing and summarizing texts. 
Your current task is to create a summary of one chapter of a book provided by the user.
The chapter tile and body are provided in the text.  In the summary, use the chapter title verbatim (do not make  up your own!) in the h2 tag.
Do not preface the summary with any text, just provide the summary in the format below.
The summary should be written in this style:
        
<h2>The Role of Family and Friends in Shaping Your Habits</h2>
<ul>
  <li><b>Laszlo Polgar's Experiment:</b>
    <ul>
      <li>Belief in hard work over innate talent.</li>
      <li>Raised his daughters to be chess prodigies through deliberate practice and good habits.</li>
      <li>Children homeschooled, immersed in chess culture, achieved remarkable success.</li>
    </ul>
  </li>
  <li><b>The Seductive Pull of Social Norms:</b>
    <ul>
      <li>Humans seek to fit in and earn approval from peers.</li>
      <li>Social norms shape behavior, making certain habits attractive.</li>
      <li>We imitate habits from family, friends, and the powerful.</li>
    </ul>
  </li>
  <li><b>Imitating the Close:</b>
    <ul>
      <li>Proximity influences behavior; we imitate habits of those closest to us.</li>
      <li>Joining a culture where desired behavior is normal can make habits more attractive.</li>
      <li>Belonging to a tribe sustains motivation and reinforces new habits.</li>
    </ul>
  </li>
  <li><b>Imitating the Many:</b>
    <ul>
      <li>Asch's conformity experiments show how individuals tend to conform to group behavior.</li>
      <li>We often follow the tribe to fit in, even if it means going against our beliefs.</li>
    </ul>
  </li>
  <li><b>Imitating the Powerful:</b>
    <ul>
      <li>We seek behaviors that earn us respect, approval, and status.</li>
      <li>We imitate high-status individuals and avoid behaviors that might lower our status.</li>
      <li>Mimicking successful behaviors can make habits more attractive.</li>
    </ul>
  </li>
</ul>

Note: The sample above is just an example.  Do not copy any content from the sample in the summary.

Also, the output should not have multiple <h2> tags.  There should be only one <h2> tag for the chapter title."""

extract_epub_content_boundaries = """You are an intelligent assistant, skilled in analyzing text documents.
You are given a list of items from an ePub book. Each item is a chapter or a section in the book.
You have to identify the item number for the start chapter and the end chapter.  
The start item should be the first core content of the book that typically follows the sections such as Table of Contents, About The Author, and Preface.
The end item should be the last core content of the book.  It should not include section such as Index, Appendix, and Acknowledgments. 

The output should be in this format:
ContentStartItem: <start_item_number>
ContentEndItem: <end_item_number>

There should be no lines before or after the output.  Only the start and end item numbers should be listed as shown above."""

extract_book_link = """You are an intelligent assistant, skilled in analyzing text documents.
You are given an HTML page which has a table of books listed in it.  Each row of the table has a link to a different PDF/EPUB/AZW3 file.
From this table, you will select a row based on the following criteria:
1) the Extension column of that row has the string 'epub'
2) if there are multiple rows with Extension 'epub', pick one of the top five rows that has the biggest file size

Once a row has been identified, extract the link to the EPUB file and output it as a single URL."""
