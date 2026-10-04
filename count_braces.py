import sys
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

idx = content.find("if (btnQueryPanel) {\n        btnQueryPanel.addEventListener('click'")
if idx == -1:
    print("NOT FOUND")
    sys.exit(0)

# count braces from idx to the end of the btnQueryPanel block
end_idx = content.find("        });\n    }", idx) + len("        });\n    }")

block = content[idx:end_idx]
print(f"Braces in block: {block.count('{')} open, {block.count('}')} close")
