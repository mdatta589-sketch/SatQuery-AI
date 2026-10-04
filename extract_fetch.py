import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

fetches = re.findall(r'fetch\([\'\"\]+(.*?)[\'\"\]+', code)
for f in fetches:
    print(f)
