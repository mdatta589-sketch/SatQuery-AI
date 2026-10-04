import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('map.on(L.Draw.Event.CREATED')
end = js.find('updateAOIPanel();', start) + 20
print(js[start:end])
