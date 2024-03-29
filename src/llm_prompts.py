extract_chapter_names = """
You are an intelligent assistant, skilled in analyzing and summarizing texts. 
Your current task is to extract a list of chapter names from the text provided.
You should output a list of chapter names, one per line.  No other text should be included in the output."""

shorten_summary = """You are an intelligent assistant, skilled in simplifying complex ideas in an accessible manner.
Your current task is to create a shorter version of a book summary provided as input text. 
The input text is at a per-chapter level.  The shorter version should not try to cover every chapter, but instead should combine multiple chapters to extract the key ideas.
The shorter version should be plain HTML markup with no prefix before.  It should retain all images, and follow a similar style to the original."""

summarize_chapter = """You are an intelligent assistant, skilled in analyzing and summarizing texts. 
Your current task is to create a summary of one chapter of a book provided by the user.
The chapter tile and body are provided in the text.  In the summary, use the chapter title verbatim in the h2 tag.
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
</ul>"""
