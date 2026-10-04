import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.finditer(r'L.GeometryUtil', js)
for m in matches:
    print(m.group(0))
