import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('L.Draw.Rectangle')
print(js[start-100:start+200])
