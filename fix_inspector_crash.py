import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Remove the offending lines
content = content.replace("document.getElementById('inspector-content').style.display = 'none';", "")
content = content.replace("document.getElementById('inspector-empty').style.display = 'block';", "")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REMOVED OFFENDING LINES")
