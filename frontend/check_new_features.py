import sys
with open('new_features.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('map.on(L.Draw.Event.CREATED')
print(js[start:start+1000])
