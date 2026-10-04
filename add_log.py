with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace("        btnQueryPanel.addEventListener('click', async () => {\n            const qInput = document.getElementById('query-input-panel');", "        btnQueryPanel.addEventListener('click', async () => {\n            console.log('Ask Query Button Clicked!');\n            const qInput = document.getElementById('query-input-panel');")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("ADDED LOG")
