import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('list-analysis:', bool(re.search(r'id=[\'"]list-analysis[\'"]', html)))
print('group-analysis:', bool(re.search(r'id=[\'"]group-analysis[\'"]', html)))
