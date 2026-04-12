import json

NOTEBOOK = "genre_wordclouds-3.ipynb"
OUTPUT   = "wordclouds.html"

IMAGE_CELLS = {
    11: {"tag": "Overall Genres", "title": "Genre Preferences Across All Students", "desc": "Three views of genre preferences: students top-ranked genre, all top-3 picks combined, and genres they attend concerts for."},
    13: {"tag": "Genres by College", "title": "Genre Preferences Broken Down by College", "desc": "Each college at Northeastern shows distinct genre preferences, reflecting different student backgrounds."},
    15: {"tag": "Overall Artists", "title": "Most Popular Artists Among All Students", "desc": "Every artist mentioned in students top picks, sized by total mentions."},
    17: {"tag": "Artists by College", "title": "Top Artists Broken Down by College", "desc": "Artist preferences vary by college, revealing niche preferences that aggregate data would miss."},
}

with open(NOTEBOOK, "r") as f:
    nb = json.load(f)

sections_html = ""
for cell_idx, meta in IMAGE_CELLS.items():
    cell = nb["cells"][cell_idx]
    b64 = None
    for output in cell.get("outputs", []):
        if "image/png" in output.get("data", {}):
            raw = output["data"]["image/png"]
            b64 = "".join(raw) if isinstance(raw, list) else raw
            break
    if not b64:
        print(f"Warning: no image in cell {cell_idx}")
        continue
    sections_html += f'<div class="wc-section"><span class="wc-tag">{meta["tag"]}</span><h2>{meta["title"]}</h2><p>{meta["desc"]}</p><img src="data:image/png;base64,{b64}" alt="{meta["title"]}" /></div><hr class="divider">'

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Word Clouds - NEU Music Survey</title>
  <link rel="stylesheet" href="style.css">
  <style>
    .wc-section {{ margin: 50px auto; max-width: 960px; padding: 0 20px; }}
    .wc-section h2 {{ font-size: 1.4rem; font-weight: 600; margin-bottom: 8px; color: #222; }}
    .wc-section p {{ color: #555; font-size: 0.97rem; line-height: 1.6; margin-bottom: 16px; }}
    .wc-section img {{ width: 100%; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
    .wc-tag {{ display: inline-block; background: #f0f0f0; color: #555; font-size: 0.78rem; padding: 3px 10px; border-radius: 12px; margin-bottom: 12px; }}
    .page-header {{ text-align: center; padding: 50px 20px 20px; }}
    .page-header h1 {{ font-size: 2rem; font-weight: 700; color: #111; }}
    .page-header p {{ color: #666; font-size: 1rem; max-width: 600px; margin: 12px auto 0; line-height: 1.6; }}
    hr.divider {{ border: none; border-top: 1px solid #eee; margin: 40px auto; max-width: 960px; }}
  </style>
</head>
<body>
  <nav>
    <a href="index.html">Home</a>
    <a href="sankey.html">Sankey Diagram</a>
    <a href="treemap.html">Treemap Diagram</a>
    <a href="wordclouds.html">Word Clouds</a>
    <a href="cloud.html">Cloud Diagram</a>
    <a href="regression.html">Regression Diagram</a>
    <a href="conclusions.html">Conclusions</a>
  </nav>
  <div class="page-header">
    <h1>Word Cloud Visualizations</h1>
    <p>Generated from Northeastern University student music survey responses.</p>
  </div>
  {sections_html}
</body>
</html>"""

with open(OUTPUT, "w") as f:
    f.write(html)
print("Done! wordclouds.html created!")
