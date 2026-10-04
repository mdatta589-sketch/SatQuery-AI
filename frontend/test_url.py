import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

match = re.search(r'fetch\([\'"](.*upload)[\'"]', js)
print(repr(match.group(1)))
