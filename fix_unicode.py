import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Replace any corrupted unicode with an em-dash
content = re.sub(r'\?"', '—', content)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED CORRUPT UNICODE")
