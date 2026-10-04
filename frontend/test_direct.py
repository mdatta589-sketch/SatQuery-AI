import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html_ids = set(re.findall(r'id=[\'"](.*?)[\'"]', html))

# Find all direct addEventListener calls
matches = re.findall(r'getElementById\([\'"](.*?)[\'"]\)\.addEventListener', js)

missing = []
for m in matches:
    if m not in html_ids:
        missing.append(m)

print("IDs with direct addEventListener but not in HTML:", missing)
