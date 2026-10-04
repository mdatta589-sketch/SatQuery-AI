import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find("document.getElementById('geotiff-upload').addEventListener('change'")
end = start
open_braces = 0
found_open = False
for i in range(start, len(js)):
    if js[i] == '{':
        open_braces += 1
        found_open = True
    elif js[i] == '}':
        open_braces -= 1
    
    if found_open and open_braces == 0:
        end = i
        break

sys.stdout.reconfigure(encoding='utf-8')
print(js[start:end+2])
