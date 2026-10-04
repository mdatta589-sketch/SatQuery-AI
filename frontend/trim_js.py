with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js.rstrip() + '\n')
