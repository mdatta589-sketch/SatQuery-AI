import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="inspector-panel"')
print(html[start:start+1000])
