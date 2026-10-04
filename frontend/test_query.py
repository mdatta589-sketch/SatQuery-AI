import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'<div class="query-container">.*?</div>', html, flags=re.DOTALL)
if match:
    print(match.group(0))
else:
    print('Not found')
