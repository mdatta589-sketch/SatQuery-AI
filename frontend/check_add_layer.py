import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function addLayerToList')
if start == -1:
    print('addLayerToList not found')
else:
    print(js[start:start+1500])
