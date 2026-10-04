import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function initMap()')
end = js.find('// ==== UI Helpers ====', start)
print(js[start:start+1000])
