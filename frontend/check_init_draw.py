import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('drawnItems = new L.FeatureGroup();')
end = js.find('L.control.zoom', start)
print(js[start:end])
