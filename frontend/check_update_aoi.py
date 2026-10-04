import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function updateAOIPanel()')
end = js.find('function updateNoDataState()', start)
print(js[start:end])
