import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

ids_in_html = re.findall(r'id=[\'"](.*?)[\'"]', html)

missing = []
for html_id in ids_in_html:
    if f"getElementById('{html_id}')" not in js and f'getElementById("{html_id}")' not in js:
        missing.append(html_id)

print(f'HTML IDs not referenced in JS: {missing}')
