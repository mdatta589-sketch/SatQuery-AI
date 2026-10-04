import re
with open('app.js', 'rb') as f:
    js = f.read()
match = re.search(b'fetch\([\'"](.*upload)[\'"]', js)
print(match.group(1))
