from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

# Load your JSON data here (you can replace this with reading from a file)
with open("data/substantives.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

# Prepare a simple HTML template with placeholders
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{word}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
  .container {{ max-width: 900px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; }}
  h1 {{ margin-top: 0; text-align: center; color: #4CAF50; }}
  h2 {{ margin-top: 30px; border-bottom: 2px solid #ccc; padding-bottom: 5px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
  th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
  th {{ background-color: #eee; }}
  .info {{ margin-top: 10px; }}
  .tags-notes {{ display: flex; justify-content: space-between; margin-top: 10px; }}
  .tags, .notes {{ width: 48%; background: #fafafa; padding: 10px; border-radius: 4px; }}
  .section {{ margin-top: 30px; }}
</style>
</head>
<body>
<div class="container">
  <h1>{word} ({gender})</h1>
  <h2>{translation}</h2>
  
  <div class="tags-notes">
    <div class="tags"><strong>Tags:</strong> {tags}</div>
    <div class="notes"><strong>Notes:</strong> {notes}</div>
  </div>
  
  <div class="section">
    <h2>Declination</h2>
    <table>
      <thead>
        <tr>
          <th>Case</th>
          <th>Singular</th>
          <th>Plural</th>
        </tr>
      </thead>
      <tbody>
        {cases_rows}
      </tbody>
    </table>
  </div>
  
  <div class="section">
    <h2>Examples</h2>
    <table>
      <thead>
        <tr>
          <th> </th>
          <th> </th>
        </tr>
      </thead>
      <tbody>
        {examples_rows}
      </tbody>
    </table>
  </div>
</div>
</body>
</html>
"""

@app.get("/")
async def root():
    return {"msg": "i am alive"}


@app.get("/{word_id}", response_class=HTMLResponse)
async def get_word(word_id: int):
    
    # Find the data by ID
    data = next((d for d in data_list if d["id"] == word_id), None)
    if not data:
        return HTMLResponse(content=f"<h1>Word not found</h1>", status_code=404)
    
    # Generate cases rows
    cases_html = ""
    for case_name, forms in data["grammar"].items():
        cases_html += f"<tr><td>{case_name.capitalize()}</td><td>{forms[0]}</td><td>{forms[1]}</td></tr>"

    # Generate example rows
    examples_html = ""
    for e1, e2 in zip(data["examples"]["language_1"], data["examples"]["language_2"]):
        examples_html += f"<tr><td>{e1}</td><td>{e2}</td></tr>"
    
    # Fill the template with actual data
    html_content = html_template.format(
        word=data["word"],
        translation=data["translation"],
        tags=", ".join(data["tags"]),
        notes=data["notes"],
        gender=data["gender"],
        cases_rows=cases_html,
        examples_rows=examples_html
    )

    return HTMLResponse(content=html_content)

# To run: uvicorn main:app --reload
