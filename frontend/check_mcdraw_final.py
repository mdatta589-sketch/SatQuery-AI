import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('const mcDraw = document.getElementById(\'mc-draw\');')
end = js.find('const mcMeasure', start)
print(js[start:end])
