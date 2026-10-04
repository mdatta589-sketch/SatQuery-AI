import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('fetch(')
end = js.find(')', start)
sys.stdout.reconfigure(encoding='utf-8')
print(js[start-50:end+50])
