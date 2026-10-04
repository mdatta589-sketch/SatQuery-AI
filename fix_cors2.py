import re

with open('backend/app/main.py', 'r', encoding='utf8') as f:
    content = f.read()

content = re.sub(
    r'allow_origins=\[.*?\]',
    'allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:8080", "http://localhost:8080"]',
    content,
    flags=re.DOTALL
)

with open('backend/app/main.py', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED main.py")
