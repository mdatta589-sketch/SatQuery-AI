import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('/api/v1/catalog/search')
print(js[start-500:start+1000])
