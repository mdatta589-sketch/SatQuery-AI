with open('frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("resolution: currentLayer.metadata?.resolution ?  m : '-'", "resolution: currentLayer.metadata?.resolution ? \\ m\ : '-'")

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
