import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<main class="main-content">')
end = html.find('</main>', start)
print(html[start:start+1000])
