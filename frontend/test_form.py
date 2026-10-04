import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.finditer(r'<form', html)
for m in matches:
    print(f"Form found at {m.start()}")
