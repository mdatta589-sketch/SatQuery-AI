import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

urls = re.findall(r'fetch\([\'"](.*?)[\'"]', js)
for url in urls:
    print(url)
