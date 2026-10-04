import sys
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<footer class="app-footer">')
end = html.find('</footer>', start)
print(html[start:end+9])
