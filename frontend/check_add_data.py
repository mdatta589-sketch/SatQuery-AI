import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add Data click
matches = re.findall(r'btn-add-data.*?\}', js, flags=re.DOTALL)
if matches: print("btn-add-data handler:", matches[0][:200])

# File upload
match2 = re.search(r'geotiff-upload[\'"].*?addEventListener[\s\S]*?fetch\([\'"](.*?)[\'"]', js)
if match2: print("Upload URL:", match2.group(1))

