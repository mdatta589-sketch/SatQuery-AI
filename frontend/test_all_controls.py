import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

controls = re.findall(r'<(?:button|input|select)[^>]*id=[\'"](.*?)[\'"]', html)
print(controls)
