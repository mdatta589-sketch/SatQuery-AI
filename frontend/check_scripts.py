import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.finditer(r'<script.*?>', html)
for m in matches:
    print(m.group(0))
