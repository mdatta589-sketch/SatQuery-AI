import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('drawnItems = new L.FeatureGroup();')
print(js[start:start+500])
