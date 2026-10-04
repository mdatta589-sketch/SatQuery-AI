import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function selectLayer')
end = js.find('function populateInspector')
sys.stdout.reconfigure(encoding='utf-8')
print(js[start:end])
