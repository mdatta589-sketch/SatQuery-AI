import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('geotiff-upload')
sys.stdout.reconfigure(encoding='utf-8')
print(js[start:start+1000])
