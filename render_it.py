import argparse
import json
from jinja2 import Environment, FileSystemLoader
import sys
from unidecode import unidecode
import qrcode
import os
from dotenv import load_dotenv

load_dotenv()

########  C O N S T A N T S ###########

# URL Template
url_root = f"http://{os.getenv('local_ip')}:8002/"

# destination directory
dest_dir = "rendered_html/"

# qr dest
qr_dest = "qrs/"

#######################################

# Load JSON data once at startup
with open("vocab_data.json", "r", encoding="utf-8") as f:
    vocab_data = json.load(f)

# read cli arguments:
parser = argparse.ArgumentParser(description="Render vocabulary for a single word")
parser.add_argument("--word", help="Word to search for in the vocabulary(optional), if ommited render all", default=None)

args = parser.parse_args()

# prepare template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("vocab_template.html")

# one single word or all?
if args.word:
    # Find the specific word:
    found_word = next((item for item in vocab_data if item["word"].lower() == args.word.lower()), None)
    if not found_word:
        print(f"Word '{args.word}' not found in the JSON data.")
        sys.exit(1)

    entries = [found_word]

else:
    # render all words from json file
    entries = [item for item in vocab_data]


for entry in entries:
    # Render template to string
    html_str = template.render(request={}, vocabulary=[entry])
    file_name = unidecode(entry["word"])

    # Generate QR code
    qr = qrcode.make(f"{url_root}{file_name}.html")

    # Save the QR code image
    qr.save(f"{qr_dest}{file_name}.png")
    print(f"QR-Code for {file_name} generated. Saved to {qr_dest}")

    # Save html content to file
    with open(f"{dest_dir}{file_name}.html", "w", encoding="utf-8") as f:
        f.write(html_str)

    print(f"HTML for {entry['word']} saved to {dest_dir}{file_name}.html")
