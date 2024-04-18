# a zsh script that publishes all summaries to the public website
# Usage: ./publish.sh

cp output/* ../book-summarizer-output/
cd ../book-summarizer-output/
git add .
git commit -m "added new summaries"
git push
cd ../book-summarizer/
