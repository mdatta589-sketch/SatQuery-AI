with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

lines = js.split('\n')
for i, line in enumerate(lines):
    if 'id: nalysis:ndvi:' in line:
        lines[i+1] = "                  name: NDVI - ,"

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
