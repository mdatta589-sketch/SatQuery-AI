import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

bad_lines = '''                document.getElementById('inspector-empty').style.display = 'none';
                document.getElementById('inspector-content').style.display = 'block';'''

content = content.replace(bad_lines, "")
with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED CRASH")
