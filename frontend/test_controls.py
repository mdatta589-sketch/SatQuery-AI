import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

controls = re.findall(r'<(?:button|input|select)[^>]*id=[\'"](.*?)[\'"]', html)

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

missing = []
for cid in controls:
    if f"'{cid}'" not in js and f'"{cid}"' not in js and cid not in ['basemap-toggle']:
        missing.append(cid)

print('Controls missing handlers:', missing)
