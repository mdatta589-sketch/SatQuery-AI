import re

with open('frontend/index.html', 'r', encoding='utf8') as f:
    content = f.read()

content = re.sub(r'app\.js\?v=\w+', 'app.js?v=20261004d', content)

with open('frontend/index.html', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED index.html")
