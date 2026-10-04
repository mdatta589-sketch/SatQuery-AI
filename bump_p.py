with open('frontend/index.html', 'r', encoding='utf8') as f:
    content = f.read()
import re
content = re.sub(r'app\.js\?v=\w+', 'app.js?v=20261004p', content)
with open('frontend/index.html', 'w', encoding='utf8') as f:
    f.write(content)
