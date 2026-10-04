import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html_ids = set(re.findall(r'id=[\'"](.*?)[\'"]', html))

# Find all variables assigned to getElementById
assignments = re.findall(r'(\w+)\s*=\s*document\.getElementById\([\'"](.*?)[\'"]\)', js)

missing = []
for var_name, el_id in assignments:
    if el_id not in html_ids:
        # Check if this variable is used with addEventListener without an if check
        # We'll just flag if it's missing from HTML first
        missing.append((var_name, el_id))

print("Variables assigned to missing HTML IDs:", missing)
