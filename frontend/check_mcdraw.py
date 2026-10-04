import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('mcDraw.addEventListener')
end = js.find('});', start)
print(js[start-50:end+20])
