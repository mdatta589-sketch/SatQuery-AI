import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function updateNoDataState()')
end = js.find('}', start)
while True:
    next_close = js.find('}', end + 1)
    if 'function ' in js[end:next_close]:
        break
    if next_close == -1:
        break
    end = next_close

sys.stdout.reconfigure(encoding='utf-8')
print(js[start:end+1])
