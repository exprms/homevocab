import argparse
import json
from jinja2 import Environment, FileSystemLoader
import sys

# destination directory
dest_dir = "rendered_html"

# Load JSON data once at startup
with open("vocab_data.json", "r", encoding="utf-8") as f:
    vocab_data = json.load(f)

# print(vocab_data)
parser = argparse.ArgumentParser(description="Render vocabulary for a single word")
parser.add_argument("--word", help="Word to search for in the vocabulary(optional), if ommited render all", default=None)
# parser.add_argument("--output", help="Output filename to save HTML (optional)", default=None)

args = parser.parse_args()

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("vocab_template.html")

if args.word:
    # Find the entry
    found_word = next((item for item in vocab_data if item["word"].lower() == args.word.lower()), None)
    if not entry:
        print(f"Word '{args.word}' not found in the JSON data.")
        sys.exit(1)

    print(found_word)
    entries = [found_word]
else:
    entries = [item for item in vocab_data]
print(entries)
for entry in entries:
    # Render template to string
    html_str = template.render(request={}, vocabulary=[entry])

    # Save to file
    with open(f"{dest_dir}/{entry['word']}.html", "w", encoding="utf-8") as f:
        f.write(html_str)

    print(f"HTML for {entry['word']} saved to {entry['word']}.html")
