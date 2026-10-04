import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="geotiff-upload"')
print(html[start-200:start+200])
