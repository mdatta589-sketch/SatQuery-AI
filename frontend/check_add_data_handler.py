import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('geotiff-upload')
print(js[start:start+2000])
