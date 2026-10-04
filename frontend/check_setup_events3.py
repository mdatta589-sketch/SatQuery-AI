import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function setupEventListeners()')
end = js.find('document.getElementById(\'btn-add-data\')', start)
print(js[start:end+500])
