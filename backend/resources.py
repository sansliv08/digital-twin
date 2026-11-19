import json

# Read master CV (Markdown)
try:
    with open("./data/lara_curriculo_mestre.md", "r", encoding="utf-8") as f:
        lara_curriculo_mestre = f.read()
except FileNotFoundError:
    lara_curriculo_mestre = "Curriculum not available"

# Read other data files
with open("./data/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

with open("./data/style.txt", "r", encoding="utf-8") as f:
    style = f.read()

with open("./data/facts.json", "r", encoding="utf-8") as f:
    facts = json.load(f)