import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="group-uploaded"')
end = html.find('id="group-stac"')
sys.stdout.reconfigure(encoding='utf-8')
print(html[start:end])
