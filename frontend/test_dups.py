import re
from collections import Counter

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids = re.findall(r'id=[\'"](.*?)[\'"]', html)
c = Counter(ids)
dups = [k for k, v in c.items() if v > 1]
print('Duplicate IDs:', dups)
