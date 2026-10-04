import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('list-uploaded:', bool(re.search(r'id=[\'"]list-uploaded[\'"]', html)))
print('group-uploaded:', bool(re.search(r'id=[\'"]group-uploaded[\'"]', html)))
print('list-stac:', bool(re.search(r'id=[\'"]list-stac[\'"]', html)))
print('group-stac:', bool(re.search(r'id=[\'"]group-stac[\'"]', html)))
