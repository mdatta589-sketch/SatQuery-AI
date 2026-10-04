import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('const bbox = [bounds.getWest()')
print(js[start-200:start+200])
