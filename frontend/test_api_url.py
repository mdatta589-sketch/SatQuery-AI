import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

matches = re.finditer(r'API_URL|const API|http', js)
for m in matches:
    start = max(0, m.start() - 20)
    end = min(len(js), m.end() + 20)
    print(js[start:end])
