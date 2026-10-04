import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.finditer(r'<aside class="panel-right">', html)
for m in matches:
    print(html[m.start()+2000:m.start()+4000])
