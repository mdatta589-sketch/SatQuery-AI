import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

match = re.search(r'function setupEventListeners\(\) \{(.*?)\n\}', js, flags=re.DOTALL)
if match:
    ids = re.findall(r'getElementById\([\'"](.*?)[\'"]\)\.addEventListener', match.group(1))
    print(ids)
else:
    print('Not found')
