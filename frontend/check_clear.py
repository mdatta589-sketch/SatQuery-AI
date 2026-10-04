import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function clearLayerList')
if start == -1:
    print('clearLayerList not found')
else:
    print(js[start:start+500])
