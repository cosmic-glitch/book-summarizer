
# HLD
Come up with a high level design of a web application called Book Summarizer.  Decide what frameworks, libraries, and hosting services should be used.

The app will consist of a batch process to generate book summaries, and a web frontend to serve those summaries to users as static HTML files.

The offline batch process will kick off at some regular cadence (say once every day).  It will check if any new PDF books have been added to a fixed “library” folder since the last run.  For every new book that has been added, the batch process will generate a multi-page summary as a single HTML file.  The summary will be generated for each chapter in the book separately.  OpenAI’s GPT model will be used to generate the summary.  The model will be promoted to create summaries that extract the key points and insights in each chapter.

The app will have a web frontend.  The front end will consist of just a bunch of links - one for each book.  When a link is clicked, the user will be taken to the summary HTML for that book.