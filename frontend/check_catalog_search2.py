import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('const req = {')
print(js[start-800:start])
