import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

matches = re.finditer(r'geotiff-upload', js)
for m in matches:
    start = max(0, m.start() - 50)
    end = min(len(js), m.end() + 50)
    print(f"--- MATCH ---")
    print(js[start:end])
